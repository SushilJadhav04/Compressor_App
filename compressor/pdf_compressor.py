import pikepdf
from io import BytesIO

def compress_pdf(uploaded_file, target_size_kb=500):
    target_bytes = target_size_kb * 1024
    quality_options = [
        pikepdf.CompressionLevel.compression_level_fast,
        pikepdf.CompressionLevel.default,
        pikepdf.CompressionLevel.compression_level_max
    ]

    best_output = None
    best_diff = float("inf")

    try:
        original_pdf = pikepdf.open(uploaded_file)

        for compression in quality_options:
            out_io = BytesIO()
            original_pdf.save(out_io, 
                compress_streams=True, 
                object_stream_mode=pikepdf.ObjectStreamMode.generate,
                compression=compression
            )

            size = len(out_io.getvalue())
            diff = abs(size - target_bytes)

            if diff < best_diff:
                best_output = out_io
                best_diff = diff

    except Exception as e:
        print(f"[ERROR] PDF compression failed: {e}")
        uploaded_file.seek(0)
        return uploaded_file

    if best_output:
        best_output.seek(0)
        return best_output
    else:
        uploaded_file.seek(0)
        return uploaded_file
