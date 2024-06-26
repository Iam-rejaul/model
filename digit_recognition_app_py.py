# -*- coding: utf-8 -*-
"""digit_recognition_app.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1TE-5A6fWRNVvAtoPjH8Uh3OF6GzQ3GlK
"""

from google.colab import drive
drive.mount('/content/drive')



import streamlit as st
import cv2
import numpy as np
import tensorflow as tf  # Import TensorFlow at the beginning

# Load your saved model (replace with your model's path)
model = tf.keras.models.load_model('model.h5')

def predict_digit(image):
  # Preprocess the image (resize, normalize, etc.) based on your model's requirements
  processed_image = image.reshape(1,28,28,1)/255.0  # Your image preprocessing logic here
  prediction = model.predict(processed_image)
  return np.argmax(prediction)  # Get the class with the highest probability

st.title('Digit Recognition Web App')

# Create an empty element
canvas = st.empty()

# Although you can't directly use getContext(), you can leverage JavaScript within Streamlit
canvas.write("""
<canvas id="myCanvas" width="280" height="280" style="background-color: black;"></canvas>
<script>
  const canvas = document.getElementById('myCanvas');
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = 'white'; // Set drawing color (matches training data)
  ctx.lineWidth = 10; // Adjust brush width

  let isDrawing = false;
  let x0, y0;

  canvas.onmousedown = function(e) {
    isDrawing = true;
    x0 = e.offsetX;
    y0 = e.offsetY;
  };

  canvas.onmouseup = function() {
    isDrawing = false;
  };

  canvas.onmousemove = function(e) {
    if (isDrawing) {
      const x1 = e.offsetX;
      const y1 = e.offsetY;
      ctx.beginPath();
      ctx.moveTo(x0, y0);
      ctx.lineTo(x1, y1);
      ctx.stroke();
      x0 = x1;
      y0 = y1;
    }
  };
</script>
""", unsafe_allow_html=True)  # Allow unsafe HTML for canvas creation

# Button to clear the canvas
clear_button = st.button('Clear Canvas')
if clear_button:
  canvas.empty()  # Clear the element's content
  canvas.write("""
  <canvas id="myCanvas" width="280" height="280" style="background-color: black;"></canvas>
  <script>
    // ... Same JavaScript code for drawing functionality ...
  </script>
""", unsafe_allow_html=True)  # Recreate canvas and script

# Button to predict
predict_button = st.button('Predict Digit')
if predict_button:
  # Get the canvas data as an image
  image_data = canvas.toDataURL(type='image/png')
  image_array = np.asarray(bytearray(image_data[22:]), dtype=np.uint8)  # Extract data from base64 string
  image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

  # Preprocess the image
  processed_image = image.reshape(1,28,28,1)/255.0  # Your image preprocessing logic here

  prediction = predict_digit(processed_image)
  st.write(f"Predicted digit: {prediction}")

! streamlit run digit_recognition.py

