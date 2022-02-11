import os
import zipfile

import logg
import cv2
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

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

    bar_directory = 'bar'
    if not os.path.exists(bar_directory):
        os.makedirs(bar_directory)

    path_best_model = './best_model.h5'

    path_best_model1 = './Copy of best_model_conv.h5'

    path_to_zip_file = './Copy of best_model_resne_augm.h5.zip'

    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall('./')
    path_best_model2 = './Copy of best_model_resne_augm.h5'

    loaded_model_1 = tf.keras.models.load_model(path_best_model1)
    loaded_model_2 = tf.keras.models.load_model(path_best_model2)

    x_tick = ['50-250', '250-500', '500-750', '750-1000', '1000-1250', '1250-1500', '1500-1750', '1750-2000', '2000-2250', '2250-2500', '2500-2750', '2750-3000', '3000-3250', '3250-3500', '3500-3750', '3750-4000', '4000-4250', '4250-4500', '4500-4750', '4750-5000']

    log = logg.setup_logging('Service')
    log = logg.get_log("Service_for_load_video")
    video_name = 'train.mp4'
    vidcap = cv2.VideoCapture('video/'+video_name)
    success, image = vidcap.read()
    count = 0
    while success:
        predict = predict_result(image)
        np.save(f'./result/predict_{video_name.split(".")[0]}_frame_{count}.npy', predict)

        # # X-axis values
        # x = x_tick
        #
        # # Y-axis values
        # y = predict[0]
        #
        # # Function to plot
        # plt.figure(figsize=(10, 10))
        # plt.bar(x, y)
        # # Function add a legend
        # plt.legend(['count elements'])
        # plt.xticks(rotation=45, ha='right', va='top')
        #
        # url = f'./bar/predict_{video_name.split(".")[0]}_frame_{count}.png'
        #
        # plt.savefig(url)
        # plt.clf()
        # plt.cla()
        success, image = vidcap.read()
        count += 1
