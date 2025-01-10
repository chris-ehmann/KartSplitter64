import numpy as np
import cv2 as cv
import math
from keras.models import load_model
from keras.applications.resnet50 import preprocess_input
from timeit import default_timer as timer

IMAGE_SIZE = (160, 160)

def load(dir):
    model = load_model(dir)
    return model

def predict(input, model):

    validation = np.stack([preprocess_input(cv.resize(input, IMAGE_SIZE))])
    probs = model.predict(validation, verbose=0)

    return probs

def warm_up(model):
    img = cv.imread("../templates/misc/player_select.png")
    predict(img, model)

    return True

def set_prediction_time(model):
    img = cv.imread("../templates/misc/player_select.png")

    start_time = timer()
    predict(img, model)
    end_time = timer()

    prediction_time_ms = math.ceil((end_time - start_time) * 1000)
    return prediction_time_ms

