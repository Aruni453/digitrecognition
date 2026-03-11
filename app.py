import streamlit as st
import tensorflow as tf
import numpy as np
import cv2
from PIL import Image
import os

# ... your CSS and title code remains unchanged ...

@st.cache_resource(show_spinner=False)
def load_model():
    model_path = "mnist_cnn_model.h5"
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file '{model_path}' not found.")
    model = tf.keras.models.load_model(model_path, compile=False)
    return model

try:
    model = load_model()
except Exception as e:
    st.error(f"Error loading model: {str(e)}")
    st.stop()

file = st.file_uploader("📤 Upload Digit Image", type=["png","jpg","jpeg"])

if file:
    col1, col2 = st.columns(2)

    img = Image.open(file).convert("L")
    img_array = np.array(img)

    img_resized = cv2.resize(img_array,(28,28))
    img_norm = img_resized/255.0
    img_input = img_norm.reshape(1,28,28,1)

    prediction = model.predict(img_input)
    digit = np.argmax(prediction)
    confidence = np.max(prediction) * 100

    with col1:
        st.subheader("Uploaded Image")
        st.image(img, width=200)

    with col2:
        st.subheader("Prediction Result")
        st.markdown(f"""
        <div class="prediction-box">
        Predicted Digit: {digit} <br>
        Confidence: {confidence:.2f}%
        </div>
        """, unsafe_allow_html=True)

    st.subheader("Confidence")
    st.progress(min(100, int(confidence)))