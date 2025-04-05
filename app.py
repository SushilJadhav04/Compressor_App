import streamlit as st
from compressor.image_compressor import compress_image
from compressor.pdf_compressor import compress_pdf

st.set_page_config(page_title="🗜️ File Compressor", layout="centered")
st.title("📦 Image & PDF Compressor")

uploaded_file = st.file_uploader("Upload an image or PDF", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file:
    file_type = "Image" if uploaded_file.type.startswith("image") else "PDF"
    st.write(f"Detected file type: **{file_type}**")

    if file_type == "Image":
        quality = st.slider("Select Compression Quality (lower = smaller size)", 10, 100, 60, step=10)

    if st.button("🔽 Compress & Download"):
        if file_type == "Image":
            result = compress_image(uploaded_file, quality=quality)
            st.success("✅ Image compressed!")
            st.download_button("Download Image", result, file_name="compressed_image.jpg")

        elif file_type == "PDF":
            result = compress_pdf(uploaded_file)
            st.success("✅ PDF compressed!")
            st.download_button("Download PDF", result, file_name="compressed_pdf.pdf")
