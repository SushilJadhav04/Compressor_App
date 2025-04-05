import pikepdf
from io import BytesIO

def compress_pdf(uploaded_file):
    pdf = pikepdf.open(uploaded_file)
    out_io = BytesIO()
    pdf.save(out_io)  # Removed compression param
    out_io.seek(0)
    return out_io
