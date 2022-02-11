import os

import logg
import cv2
import tensorflow as tf
import numpy as np

def predict_result(img):
    width = 720
    height = 576

    DIM = (width, height)

    frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    frame = cv2.resize(frame, DIM, interpolation=cv2.INTER_AREA) / 255.0
    frame = np.array([frame])

    predicted = (loaded_model_1.predict(frame) + loaded_model_2.predict(frame)) / 2
    predicted = predicted.astype(int)

    return predicted


if __name__ == "__main__":

    log_directory = 'log'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    path_best_model = './best_model.h5'

    loaded_model_1 = tf.keras.models.load_model(path_best_model)
    loaded_model_2 = tf.keras.models.load_model(path_best_model)

    log = logg.setup_logging('Service')
    log = logg.get_log("Service_for_load_video")
    video_name = 'train.mp4'
    vidcap = cv2.VideoCapture('video/'+video_name)
    success, image = vidcap.read()
    count = 0
    while success:
        np.save(f'./result/predict_{video_name.split(".")[0]}_frame_{count}.npy', predict_result(image))
        success, image = vidcap.read()
        count += 1
