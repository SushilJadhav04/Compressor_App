from PIL import Image
from io import BytesIO

def compress_image(uploaded_file, target_size_kb=200):
    image = Image.open(uploaded_file)

    if image.mode != "RGB":
        image = image.convert("RGB")

    min_quality = 10
    max_quality = 95
    best_quality = min_quality
    best_result = None
    target_bytes = target_size_kb * 1024

    # Binary search to find best quality for target size
    while min_quality <= max_quality:
        mid_quality = (min_quality + max_quality) // 2
        img_io = BytesIO()
        image.save(img_io, format='JPEG', quality=mid_quality, optimize=True)
        size = len(img_io.getvalue())

        if size <= target_bytes:
            best_quality = mid_quality
            best_result = img_io
            min_quality = mid_quality + 1
        else:
            max_quality = mid_quality - 1

    # Fallback in case compression fails
    if best_result is None:
        best_result = BytesIO()
        image.save(best_result, format='JPEG', quality=85, optimize=True)

    best_result.seek(0)
    return best_result
