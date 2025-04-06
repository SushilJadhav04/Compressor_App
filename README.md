Features
-PDF Compression to nearest possible size using smart image-based processing.

-Image Compression with quality control using binary search.

-Lightweight, fast, and easy to use UI.

-Download compressed files with the original name appended with -compressed.

-Clean UI with Streamlit's branding and menu hidden (local or custom-hosted).

Tech Stack
Python 3.8+

Streamlit

Pillow (PIL) – for image processing

fpdf – for reconstructing compressed PDFs

pdf2image – to convert PDF pages into images

Installation
git clone https://github.com/SushilJadhav04/file-compressor-app.git
cd file-compressor-app
pip install -r requirements.txt

Run the App
streamlit run app.py
