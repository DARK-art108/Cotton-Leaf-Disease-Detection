from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np
import tensorflow as tf

import pathlib
import wget

# from tensorflow.compat.v1.compat import ConfigProto
# from tensorflow.compat.v1 import InteractiveSession
#from tensorflow.python.client.session import InteractiveSession

# config = tf.ConfigProto()
# config.gpu_options.per_process_gpu_memory_fraction = 0.2
# config.gpu_options.allow_growth = True
# session = InteractiveSession(config=config)
# Keras
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


def model_predict(img_path, model):
    print(img_path)
    img = image.load_img(img_path, target_size=(224, 224))

    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    ## Scaling
    x = x / 255
    x = np.expand_dims(x, axis=0)

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    # x = preprocess_input(x)

    preds = model.predict(x)
    preds = np.argmax(preds, axis=1)
    if preds == 0:
        preds = "The leaf is a diseased cotton leaf."
    elif preds == 1:
        preds = "The leaf is a diseased cotton plant."
    elif preds == 2:
        preds = "The leaf is a fresh cotton leaf."
    else:
        preds = "The leaf is a fresh cotton plant."

    return preds


@app.route('/', methods=['GET', 'POST'])
def index():
    # Main page
    if request.method == 'POST':
        # Get the file from post request
        print(request.files, request.form, request.args)
        f = None
        if 'image' in request.files: f = request.files['image']
        if f:
            # Save the file to ./uploads
            file_path = os.path.join(
                app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
            f.save(file_path)

            # Make prediction
            preds = model_predict(file_path, model)
            result = preds
            return render_template('index.html', result=result, img=secure_filename(f.filename))
        return render_template('index.html', result=None, err='Failed to receive file')
    # First time
    return render_template('index.html', result=None)


if __name__ == '__main__':
    app.run(port=5001, debug=True)
