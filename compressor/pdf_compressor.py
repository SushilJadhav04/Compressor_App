## Updated pdf_compressor.py
from io import BytesIO
import tempfile
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
import subprocess
import os

def compress_pdf(uploaded_file, target_size_kb, max_attempts=5):
    """
    Compresses PDF to target size using multiple strategies
    Returns: BytesIO buffer of compressed PDF
    """
    buffer = BytesIO()
    
    try:
        # Create temporary files
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_input, \
             tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_output:
            
            # Save uploaded file to temp input
            tmp_input.write(uploaded_file.getvalue())
            tmp_input_path = tmp_input.name
            tmp_output_path = tmp_output.name

            # Compression parameters
            quality = 90  # Initial image quality
            scale_factor = 0.9  # Image scaling factor
            
            for attempt in range(max_attempts):
                # Use ghostscript for effective compression
                command = [
                    'gs',
                    '-sDEVICE=pdfwrite',
                    '-dCompatibilityLevel=1.4',
                    '-dPDFSETTINGS=/screen',
                    '-dNOPAUSE',
                    '-dQUIET',
                    '-dBATCH',
                    f'-dJPEGQ={quality}',
                    f'-sOutputFile={tmp_output_path}',
                    tmp_input_path
                ]
                
                subprocess.run(command, check=True)
                
                # Check file size
                current_size = os.path.getsize(tmp_output_path) / 1024
                if current_size <= target_size_kb:
                    break
                    
                # Adjust quality for next attempt
                quality = max(30, quality - 15)
                scale_factor = max(0.5, scale_factor - 0.1)

            # Read compressed PDF into buffer
            with open(tmp_output_path, 'rb') as f:
                buffer.write(f.read())
                
    except Exception as e:
        raise RuntimeError(f"PDF compression failed: {str(e)}") from e
    finally:
        # Cleanup temporary files
        for path in [tmp_input_path, tmp_output_path]:
            if os.path.exists(path):
                os.remove(path)
    
    buffer.seek(0)
    return buffer
