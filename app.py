import streamlit as st
from compressor.image_compressor import compress_image
from compressor.pdf_compressor import compress_pdf

st.set_page_config(page_title="Image & PDF Compressor", layout="centered")
st.title("📦 Image & PDF Compressor")

uploaded_file = st.file_uploader("Upload an image or PDF", type=["jpg", "jpeg", "png", "pdf"])
file_type = st.radio("Select File Type:", options=["Image", "PDF"])

if uploaded_file and st.button("Compress"):
    if file_type == "Image":
        result = compress_image(uploaded_file)
        st.success("✅ Image compressed!")
        st.download_button("Download Image", result, file_name="compressed_image.jpg")
    elif file_type == "PDF":
        result = compress_pdf(uploaded_file)
        st.success("✅ PDF compressed!")
        st.download_button("Download PDF", result, file_name="compressed_pdf.pdf")
