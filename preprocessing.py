import cv2
import numpy as np
from PIL import Image


IMG_SIZE = 224



def preprocess_image(uploaded_file):
    """
    Preprocess an image uploaded through Streamlit.

    Input:
        uploaded_file - Streamlit UploadedFile

    Output:
        NumPy array with shape:
        (1, 224, 224, 3)
    """

   
    image = Image.open(uploaded_file).convert("RGB")

    
    image = np.array(image)

   
    image = cv2.resize(
        image,
        (IMG_SIZE, IMG_SIZE),
        interpolation=cv2.INTER_AREA
    )

    image = image.astype(np.float32) / 255.0


    image = np.expand_dims(image, axis=0)

    return image