# This is a  Python script.

import cv2
import tensorflow as tf
import numpy as np

from flask import Flask
from PIL import Image
import os
import logg
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

from flask import request, jsonify

UPLOAD_FOLDER = './'
log = None
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

data = "<h1>Кусь</h1>"
prediction = None
gbr_result = None
path_best_model = './best_model.h5'


@app.route('/')
def first_page():
    return str(data)


@app.route('/image', methods=['GET', 'POST'])
def image_read():
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'

        img = Image.open(request.files['file1'])
        img = np.array(img)
        predict = func(img)
        return str(predict)

    return '''
      <h1>Upload new File</h1>
      <form method="post" enctype="multipart/form-data">
        <input type="file" name="file1">
        <input type="submit">
      </form>
      '''


@app.route('/api/v1/resources/image', methods=['POST'])
def api_image():
    if 'file1' not in request.files:
        return 'there is no file1 in form!'

    img = Image.open(request.files['file1'])
    img = np.array(img)
    predict = func(img)
    return str(predict)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


def func(img):
    width = 720
    height = 576

    DIM = (width, height)

    frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    frame = cv2.resize(frame, DIM, interpolation=cv2.INTER_AREA) / 255.0
    frame = np.array([frame])
    # test_image = np.reshape(frame, (1, *DIM[::-1]))

    predicted = (loaded_model_1.predict(frame) + loaded_model_2.predict(frame)) / 2
    # predicted = predicted.astype(int)
    #
    # # img = cv2.imread("frame347.png")
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # test_image = np.resize(gray, (1, *DIM[::-1]))
    #
    # # imgplot = plt.imshow(gray)
    # # plt.show()
    #
    # predicted = loaded_model.predict(test_image)
    predicted = predicted.astype(int)

    return predicted


if __name__ == "__main__":

    log_directory = 'log'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    path_best_model = './best_model.h5'

    # loaded_model = tf.keras.models.load_model(path_best_model)

    loaded_model_1 = tf.keras.models.load_model(path_best_model)
    loaded_model_2 = tf.keras.models.load_model(path_best_model)

    log = logg.setup_logging('Server')
    log = logg.get_log("Web-server")

    app.run(debug=False, host='0.0.0.0', port=3067)
