from __future__ import division, print_function
import streamlit as st
from PIL import Image, ImageOps

# coding=utf-8
import sys
import os
import glob
import re
import numpy as np
import tensorflow as tf

import pathlib
import wget

from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename

# from gevent.pywsgi import WSGIServer

# Model saved with Keras model.save()
MODEL_PATH = 'model_resnet.hdf5'
MODEL_URL = 'https://github.com/DARK-art108/Cotton-Leaf-Disease-Prediction/releases/download/v1.0/model_resnet.hdf5'
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')

# Download model if not present
while not pathlib.Path(MODEL_PATH).is_file():
    print(f'Model {MODEL_PATH} not found. Downloading...')
    wget.download(MODEL_URL)

# Define a flask app
app = Flask(__name__)

# Define upload path
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Developing in the absence of TensorFlow :P (Python 3.9.0 x64)
# def load_model(aa):
#     class a:
#         @staticmethod
#         def predict(*args):
#             return 1
#     return a()

# class image:
#     @staticmethod
#     def load_img(path, target_size):
#         return 'a'

#     @staticmethod
#     def img_to_array(img):
#         return 'v'

# Load your trained model

model = load_model(MODEL_PATH)
def model_predict(img, MODEL_PATH):
    # Create the array of the right shape to feed into the keras model
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = img
    #image sizing
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    #turn the image into a numpy array
    image_array = np.asarray(image)
    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    return np.argmax(prediction, axis=1) # return position of the highest probability

st.title("Cotton Leaf Disease Prediction")
st.header("Transfer Learning Using RESNET51V2")
st.text("Upload a Cotton Leaf Disease or Non-Diseased Image")

uploaded_file = st.file_uploader("Choose a Cotton Leaf Image...", type="jpg")
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Cotton Leaf Image', use_column_width=True)
    st.write("")
    st.write("Classifying...")
    label = model_predict(image, 'model_resnet.hdf5')
    if label == 0:
        st.write("The leaf is a diseased cotton leaf.")
    elif label == 1:
        st.write("The leaf is a diseased cotton plant.")
    elif label == 2:
        st.write("The leaf is a fresh cotton leaf.")
    else:
        st.write("The leaf is a fresh cotton plant.")
