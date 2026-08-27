import streamlit as st
from preprocessing import preprocess_image


st.title("🩺 DermaAI - Preprocessing Test")


uploaded_file = st.file_uploader(
    "Upload a skin image",
    type=["jpg", "jpeg", "png"]
)


if uploaded_file is not None:

    st.image(
        uploaded_file,
        caption="Original Image",
        use_container_width=True
    )

    if st.button("Test Preprocessing"):

        processed_image = preprocess_image(uploaded_file)

        st.success("Image preprocessing completed!")

        st.write(
            "Processed image shape:",
            processed_image.shape
        )

        st.write(
            "Data type:",
            processed_image.dtype
        )

        st.write(
            "Minimum pixel value:",
            processed_image.min()
        )

        st.write(
            "Maximum pixel value:",
            processed_image.max()
        )