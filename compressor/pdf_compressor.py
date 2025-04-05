import pikepdf
from io import BytesIO

def compress_pdf(uploaded_file, target_size_kb=500):
    target_bytes = target_size_kb * 1024

    try:
        original_pdf = pikepdf.open(uploaded_file)

        # Attempt to compress streams (only light optimization)
        compressed_pdf = pikepdf.Pdf.new()
        compressed_pdf.pages.extend(original_pdf.pages)

        out_io = BytesIO()
        compressed_pdf.save(out_io, 
            compress_streams=True, 
            object_stream_mode=pikepdf.ObjectStreamMode.generate
        )

        size = len(out_io.getvalue())
        out_io.seek(0)

        # Note: result might not always meet the target size due to PDF limits
        return out_io

    except Exception as e:
        print(f"[ERROR] PDF compression failed: {e}")
        return uploaded_file
