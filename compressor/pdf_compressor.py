import pikepdf
from io import BytesIO

def compress_pdf(uploaded_file, target_size_kb=500):
    target_bytes = target_size_kb * 1024

    try:
        original_pdf = pikepdf.open(uploaded_file)

        # Loop over compression levels (roughly simulates reducing file size)
        for level in range(6):  # 0 (max) to 5 (min)
            compressed_pdf = pikepdf.Pdf.new()
            compressed_pdf.pages.extend(original_pdf.pages)

            out_io = BytesIO()
            compressed_pdf.save(out_io, 
                compress_streams=True, 
                object_stream_mode=pikepdf.ObjectStreamMode.generate,
                stream_decode_level=level
            )

            size = len(out_io.getvalue())
            if size <= target_bytes:
                print(f"[DEBUG] PDF compressed at stream level {level} to {size/1024:.2f} KB")
                out_io.seek(0)
                return out_io

        # Fallback if we can’t hit target size
        fallback_io = BytesIO()
        original_pdf.save(fallback_io)
        fallback_io.seek(0)
        return fallback_io

    except Exception as e:
        print(f"[ERROR] PDF compression failed: {e}")
        return uploaded_file
