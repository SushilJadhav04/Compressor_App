import fitz  # PyMuPDF
from PIL import Image
from fpdf import FPDF
from io import BytesIO
import tempfile
import os

def compress_pdf(uploaded_file, target_size_kb):
    target_bytes = target_size_kb * 1024
    min_quality = 10
    max_quality = 95
    best_result = None

    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    while min_quality <= max_quality:
        mid_quality = (min_quality + max_quality) // 2
        pdf = FPDF(unit="pt", format=[595.28, 841.89])  # A4 size
        temp_files = []

        for page in doc:
            pix = page.get_pixmap(dpi=150)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            temp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            img.save(temp_img.name, format="JPEG", quality=mid_quality)
            temp_files.append(temp_img.name)

        for temp_img_path in temp_files:
            pdf.add_page()
            pdf.image(temp_img_path, x=0, y=0)

        output_data = pdf.output(dest='S').encode('latin1')  # FPDF returns string, encode to bytes
        output = BytesIO(output_data)
        current_size = len(output_data)


        # Clean up temp images
        for path in temp_files:
            os.remove(path)

        if current_size <= target_bytes:
            best_result = BytesIO(output.getvalue())
            min_quality = mid_quality + 1
        else:
            max_quality = mid_quality - 1

    if best_result:
        best_result.seek(0)
        return best_result
    else:
        output.seek(0)
        return output
