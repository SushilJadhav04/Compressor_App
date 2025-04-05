import pikepdf
from io import BytesIO

def compress_pdf(uploaded_file, target_size_kb=500):
    target_bytes = target_size_kb * 1024

    try:
        pdf = pikepdf.open(uploaded_file)

        # Basic compression: remove unused objects & optimize streams
        pdf.remove_unreferenced_resources()
        out_io = BytesIO()
        pdf.save(out_io, 
            optimize_streams=True,
            compress_streams=True,
            object_stream_mode=pikepdf.ObjectStreamMode.generate
        )

        # Check final size
        final_size = len(out_io.getvalue())
        print(f"[INFO] Compressed PDF size: {final_size/1024:.2f} KB")

        out_io.seek(0)
        return out_io

    except Exception as e:
        print(f"[ERROR] PDF compression failed: {e}")
        uploaded_file.seek(0)
        return uploaded_file
