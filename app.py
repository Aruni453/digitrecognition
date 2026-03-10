import streamlit as st
import tensorflow as tf
import numpy as np
import cv2
from PIL import Image

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Digit Recognizer",
    page_icon="✍️",
    layout="centered"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

.main-title{
    font-size:40px;
    font-weight:bold;
    text-align:center;
    color:#4CAF50;
}

.sub-title{
    text-align:center;
    font-size:18px;
    color:gray;
}

.prediction-box{
    padding:20px;
    border-radius:15px;
    background-color:#f0f2f6;
    text-align:center;
    font-size:25px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Title
# -----------------------------
st.markdown('<p class="main-title">✍️ Handwritten Digit Recognition</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Upload an image of a handwritten digit (0-9)</p>', unsafe_allow_html=True)

st.write("")

# -----------------------------
# Load Model
# -----------------------------
model = tf.keras.models.load_model("mnist_cnn_model.h5", compile=False)

# -----------------------------
# File Upload
# -----------------------------
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
    confidence = np.max(prediction)*100

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

    st.write("")

    st.progress(int(confidence))
