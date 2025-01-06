import numpy as np
import cv2 as cv
import math
from keras.models import load_model
from keras.applications.resnet50 import preprocess_input
from timeit import default_timer as timer

def load(dir):
    model = load_model(dir)
    return model

def warm_up(model):
    img = cv.imread("../templates/misc/player_select.png")
    validation = np.stack([preprocess_input(cv.resize(img, (224, 224)))])
    model.predict(validation)

    return True

def set_prediction_time(model):
    img = cv.imread("../templates/misc/player_select.png")

    start_time = timer()
    validation = np.stack([preprocess_input(cv.resize(img, (224, 224)))])
    model.predict(validation)
    end_time = timer()

    prediction_time_ms = math.ceil((end_time - start_time) * 1000)
    return prediction_time_ms

def predict(input, model):

    validation = np.stack([preprocess_input(cv.resize(input, (224, 224)))])
    probs = model.predict(validation, verbose=0)

    return probs
    

