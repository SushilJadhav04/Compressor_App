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
        pdf = FPDF(unit="pt", format=[595.28, 841.89])  # A4 size in points
        temp_image_paths = []

        try:
            for i, page in enumerate(doc):
                pix = page.get_pixmap(dpi=150)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                # Save temp image
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
                img.save(temp_file.name, format="JPEG", quality=mid_quality)
                temp_image_paths.append(temp_file.name)

            for img_path in temp_image_paths:
                pdf.add_page()
                pdf.image(img_path, x=0, y=0)

            output = BytesIO()
            pdf.output(output)
            current_size = output.tell()

            if current_size <= target_bytes:
                best_result = BytesIO(output.getvalue())
                min_quality = mid_quality + 1
            else:
                max_quality = mid_quality - 1

        finally:
            # Clean up temp image files
            for path in temp_image_paths:
                if os.path.exists(path):
                    os.remove(path)

    if best_result:
        best_result.seek(0)
        return best_result
    else:
        output.seek(0)
        return output
