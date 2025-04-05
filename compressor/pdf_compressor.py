import subprocess
import tempfile
from io import BytesIO
import os

def compress_pdf(uploaded_file, target_size_kb=500):
    target_bytes = target_size_kb * 1024
    quality_levels = ["/screen", "/ebook", "/printer", "/prepress"]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_input:
        temp_input.write(uploaded_file.read())
        input_path = temp_input.name

    best_output = None
    best_diff = float("inf")

    for quality in quality_levels:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_output:
            output_path = temp_output.name

            gs_command = [
                "gs",
                "-sDEVICE=pdfwrite",
                "-dCompatibilityLevel=1.4",
                f"-dPDFSETTINGS={quality}",
                "-dNOPAUSE",
                "-dQUIET",
                "-dBATCH",
                f"-sOutputFile={output_path}",
                input_path
            ]

            try:
                subprocess.run(gs_command, check=True)
                size = os.path.getsize(output_path)
                diff = abs(target_bytes - size)

                if diff < best_diff:
                    best_diff = diff
                    with open(output_path, "rb") as f_out:
                        best_output = BytesIO(f_out.read())

            except Exception as e:
                print(f"[ERROR] Failed with {quality}: {e}")
                continue

    if best_output:
        best_output.seek(0)
        return best_output
    else:
        print("[WARNING] Returning original file as compression failed.")
        uploaded_file.seek(0)
        return uploaded_file
