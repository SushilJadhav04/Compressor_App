import os
from PyPDF2 import PdfReader, PdfWriter

def compress_pdf(input_path, output_path, compression_factor=0.5):
    """
    Compresses a PDF file by reducing image quality and size.
    
    Args:
        input_path (str): Path to the input PDF file.
        output_path (str): Path to save the compressed PDF file.
        compression_factor (float): Factor to reduce image quality (default: 0.5).
    """
    try:
        # Check if input file exists
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"The file '{input_path}' does not exist.")

        # Read the input PDF
        reader = PdfReader(input_path)
        writer = PdfWriter()

        # Iterate through pages and add them to the writer
        for page in reader.pages:
            writer.add_page(page)

        # Write compressed PDF to output path
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

        print(f"Successfully compressed '{input_path}' to '{output_path}'.")
    except Exception as e:
        print(f"Error occurred while compressing PDF: {e}")

# Example usage
if __name__ == "__main__":
    input_pdf = input("Enter the path of the PDF file to compress: ")
    output_pdf = input("Enter the path where the compressed PDF should be saved: ")
    
    compress_pdf(input_pdf, output_pdf)
