import os
from random import randrange

import logg
import ssl
import cv2
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import zipfile

from flask import Flask, render_template, request
from PIL import Image

from Result import Result

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


log = None
app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def image_read():
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'

        img = Image.open(request.files['file1'])
        img = np.array(img)
        predict = predict_result(img)
        iter = 0
        results = []
        for result in list(predict[0]):
            if iter == 0:
                results.append(Result(50, result, 250))
            else:
                results.append(Result(iter, result))
            iter = iter + 250

        return render_template("tables.html", results=results)

    return render_template("image.html")


@app.route('/histogram', methods=['GET', 'POST'])
def image_read_histogram():
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'

        iter_num = randrange(1000)
        img = Image.open(request.files['file1'])
        img = np.array(img)
        predict = predict_result(img)
        iter = 0
        results = []
        for result in list(predict[0]):
            if iter == 0:
                results.append(Result(50, result, 250))
            else:
                results.append(Result(iter, result))
            iter = iter + 250

        plt.hist(predict[0], bins=len(predict[0]))
        url = f'./static/images/new_plot{iter_num}.png'
        plt.savefig(url)

        return render_template("tables2.html", results=results, url=url)

    return render_template("image.html")

@app.route('/api/v1/resources/image', methods=['POST'])
def api_image():
    if 'file1' not in request.files:
        return 'there is no file1 in form!'

    img = Image.open(request.files['file1'])
    img = np.array(img)
    predict = predict_result(img)

    results = []
    iter = 0
    for result in list(predict[0]):

        if iter == 0:
            results.append(
                {
                    'range': '50-250',
                    'result': int(result)
                }
            )
        else:
            results.append(
                {
                    'range': f'{iter}-{iter + 250}',
                    'result': int(result)
                }
            )
        iter = iter + 250

    return {'data': results}


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


def predict_result(img):
    width = 720
    height = 576

    DIM = (width, height)

    frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    frame = cv2.resize(frame, DIM, interpolation=cv2.INTER_AREA) / 255.0
    frame = np.array([frame])

    predicted = (loaded_model_1.predict(frame) + loaded_model_2.predict(frame)) / 2
    predicted = np.round(predicted, 0)

    return predicted


if __name__ == "__main__":

    log_directory = 'log'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    images_directory = './static/images'
    if not os.path.exists(images_directory):
        os.makedirs(images_directory)

    path_best_model1 = './Copy of best_model_conv.h5'

    path_to_zip_file = 'Copy of best_model_resne_augm.h5.zip'

    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall('./')
    path_best_model2 = './Copy of best_model_resne_augm.h5'

    loaded_model_1 = tf.keras.models.load_model(path_best_model1)
    loaded_model_2 = tf.keras.models.load_model(path_best_model2)

    log = logg.setup_logging('Server')
    log = logg.get_log("Web-server")

    app.run(debug=False, host='0.0.0.0', port=3067)
