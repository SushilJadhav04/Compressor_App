from io import BytesIO
import tempfile
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
import os

def compress_pdf(uploaded_file, target_size_kb):
    """
    Compresses PDF to target size using binary search approach
    Returns: BytesIO buffer of compressed PDF
    """
    buffer = BytesIO()
    tmp_input_path = None
    tmp_output_path = None
    
    try:
        # Create temporary files
        tmp_input = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        tmp_output = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        tmp_input_path = tmp_input.name
        tmp_output_path = tmp_output.name
        
        # Save uploaded file to temp input
        tmp_input.write(uploaded_file.getvalue())
        tmp_input.close()
        tmp_output.close()

        # Binary search parameters
        min_quality = 5
        max_quality = 95
        best_quality = min_quality
        best_result = None
        target_bytes = target_size_kb * 1024

        reader = PdfReader(tmp_input_path)
        total_pages = len(reader.pages)

        while min_quality <= max_quality:
            mid_quality = (min_quality + max_quality) // 2
            writer = PdfWriter()
            
            # Process each page
            for page in reader.pages:
                writer.add_page(page)

            # Compress PDF
            writer.add_metadata(reader.metadata)
            with open(tmp_output_path, 'wb') as output_file:
                writer.write(output_file, compress_streams=True, image_compression='jpeg', 
                            jpeg_quality=mid_quality)

            current_size = os.path.getsize(tmp_output_path)
            
            if current_size <= target_bytes:
                best_quality = mid_quality
                with open(tmp_output_path, 'rb') as f:
                    best_result = BytesIO(f.read())
                min_quality = mid_quality + 1
            else:
                max_quality = mid_quality - 1

        # If compression failed to reach target, use maximum compression
        if best_result is None:
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            
            writer.add_metadata(reader.metadata)
            with open(tmp_output_path, 'wb') as output_file:
                writer.write(output_file, compress_streams=True, image_compression='jpeg', 
                            jpeg_quality=5)
            
            with open(tmp_output_path, 'rb') as f:
                best_result = BytesIO(f.read())

        buffer = best_result

    except Exception as e:
        error_msg = f"PDF compression failed: {str(e)}"
        raise RuntimeError(error_msg) from e
    finally:
        # Cleanup temporary files
        if tmp_input_path and os.path.exists(tmp_input_path):
            try:
                os.remove(tmp_input_path)
            except Exception:
                pass
        if tmp_output_path and os.path.exists(tmp_output_path):
            try:
                os.remove(tmp_output_path)
            except Exception:
                pass
    
    buffer.seek(0)
    return buffer
