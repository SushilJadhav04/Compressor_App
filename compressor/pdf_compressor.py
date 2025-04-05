## Updated pdf_compressor.py
from io import BytesIO
import tempfile
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
import subprocess
import os

def compress_pdf(uploaded_file, target_size_kb):
    """
    Compresses PDF to target size using binary search approach
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

            # Binary search parameters
            min_quality = 5
            max_quality = 95
            best_quality = min_quality
            best_result = None
            target_bytes = target_size_kb * 1024
            
            while min_quality <= max_quality:
                mid_quality = (min_quality + max_quality) // 2
                
                # Use ghostscript for compression
                command = [
                    'gs',
                    '-sDEVICE=pdfwrite',
                    '-dCompatibilityLevel=1.4',
                    '-dPDFSETTINGS=/screen',
                    '-dNOPAUSE',
                    '-dQUIET',
                    '-dBATCH',
                    f'-dJPEGQ={mid_quality}',
                    f'-sOutputFile={tmp_output_path}',
                    tmp_input_path
                ]
                
                subprocess.run(command, check=True)
                
                # Check file size
                current_size = os.path.getsize(tmp_output_path)
                
                if current_size <= target_bytes:
                    best_quality = mid_quality
                    best_result = tmp_output_path
                    min_quality = mid_quality + 1
                else:
                    max_quality = mid_quality - 1
            
            # If compression failed to reach target, use the best result or fallback
            if best_result:
                with open(best_result, 'rb') as f:
                    buffer.write(f.read())
            else:
                # Fallback to maximum compression
                command[-3] = f'-dJPEGQ=5'
                subprocess.run(command, check=True)
                with open(tmp_output_path, 'rb') as f:
                    buffer.write(f.read())

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
