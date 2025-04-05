import streamlit as st
from compressor.image_compressor import compress_image
from compressor.pdf_compressor import compress_pdf

st.set_page_config(page_title="🗜️ File Compressor", layout="centered")
st.title("Image & PDF Compressor")

uploaded_file = st.file_uploader("Upload an image or PDF", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file:
    file_type = "Image" if uploaded_file.type.startswith("image") else "PDF"
    st.write(f"Detected file type: **{file_type}**")

    target_size_kb = st.number_input(
        "🎯 Enter target size (in KB)", min_value=10, step=10, value=200
    )


    if st.button("🔽 Compress & Download"):
        if file_type == "Image":
            result = compress_image(uploaded_file, quality=quality)
            st.success("✅ Image compressed!")
            st.download_button("Download Image", result, file_name="compressed_image.jpg")

        elif file_type == "PDF":
            result = compress_pdf(uploaded_file)
            st.success("✅ PDF compressed!")
            st.download_button("Download PDF", result, file_name="compressed_pdf.pdf")
