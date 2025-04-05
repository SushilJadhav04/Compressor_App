import fitz  # PyMuPDF
from PIL import Image
from fpdf import FPDF
from io import BytesIO

def compress_pdf(uploaded_file, target_size_kb):
    target_bytes = target_size_kb * 1024
    min_quality = 10
    max_quality = 95
    best_result = None

    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    while min_quality <= max_quality:
        mid_quality = (min_quality + max_quality) // 2
        pdf = FPDF(unit="pt", format=[595.28, 841.89])  # Default A4 size
        img_buffers = []

        for page in doc:
            pix = page.get_pixmap(dpi=150)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img_buffer = BytesIO()
            img.save(img_buffer, format="JPEG", quality=mid_quality)
            img_buffer.seek(0)
            img_buffers.append(img_buffer)

        for img_buf in img_buffers:
            pdf.add_page()
            pdf.image(img_buf, x=0, y=0)

        output = BytesIO()
        pdf.output(output)
        current_size = output.tell()

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
