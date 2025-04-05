import subprocess
import tempfile
from io import BytesIO

def compress_pdf(uploaded_file, target_size_kb=500):
    target_bytes = target_size_kb * 1024

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_input:
        temp_input.write(uploaded_file.read())
        input_path = temp_input.name

    output_io = BytesIO()

    # Ghostscript compression levels:
    # /screen (low), /ebook, /printer, /prepress (high quality)
    gs_quality = "/ebook"  # reasonable default

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_output:
        output_path = temp_output.name

        gs_command = [
            "gs",
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            "-dPDFSETTINGS={}".format(gs_quality),
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            f"-sOutputFile={output_path}",
            input_path
        ]

        try:
            subprocess.run(gs_command, check=True)
            with open(output_path, "rb") as f_out:
                compressed_bytes = f_out.read()
                output_io.write(compressed_bytes)
                output_io.seek(0)
            return output_io

        except subprocess.CalledProcessError as e:
            print("[ERROR] Ghostscript compression failed:", e)
            return uploaded_file
