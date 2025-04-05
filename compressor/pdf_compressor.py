from pdf2image import convert_from_bytes
from fpdf import FPDF
from PIL import Image
from io import BytesIO

def compress_pdf(uploaded_file, target_size_kb):
    images = convert_from_bytes(uploaded_file.read(), dpi=150)
    target_bytes = target_size_kb * 1024

    min_quality = 10
    max_quality = 95
    best_pdf = None
    best_diff = float("inf")

    while min_quality <= max_quality:
        mid_quality = (min_quality + max_quality) // 2
        pdf = FPDF(unit="pt", format=[img.width, img.height])

        image_buffers = []
        for img in images:
            img_buffer = BytesIO()
            rgb_img = img.convert("RGB")
            rgb_img.save(img_buffer, format="JPEG", quality=mid_quality)
            img_buffer.seek(0)
            image_buffers.append(img_buffer)

        pdf = FPDF(unit="pt", format=[images[0].width, images[0].height])
        for buf in image_buffers:
            pdf.add_page()
            img_path = BytesIO(buf.read())
            buf.seek(0)
            pdf.image(img_path, x=0, y=0, w=images[0].width, h=images[0].height)

        output_buffer = BytesIO()
        pdf.output(output_buffer)
        current_size = output_buffer.tell()

        diff = abs(current_size - target_bytes)

        if current_size <= target_bytes:
            best_pdf = BytesIO(output_buffer.getvalue())
            best_diff = diff
            min_quality = mid_quality + 1
        else:
            max_quality = mid_quality - 1

    if best_pdf:
        best_pdf.seek(0)
        return best_pdf
    else:
        # fallback: return last compressed output
        output_buffer.seek(0)
        return output_buffer
