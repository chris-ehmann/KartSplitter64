import cv2 as cv
import numpy as np
import mss as mss
import time
import os
import pyautogui
import livesplit as ls
import template_matching
import model as m

# Constants that define the time for the model to make a prediction in milliseconds
# And the time for the console to be reset and boot to the correct screen

FAST_MODEL_PREDICTION_TIME = 0
VERIFICATION_MODEL_PREDICTION_TIME = 0
CONSOLE_RESET_TIME = 2700

def get_capture():
    input("Move mouse to top left corner of captured video, then press enter:")
    top_left_corner = pyautogui.position()
    input("Move mouse to bottom right corner of captured video, then press enter:")
    bot_right_corner = pyautogui.position()
    monitor = {"top": top_left_corner.y, "left": top_left_corner.x, "width": bot_right_corner.x - top_left_corner.x, "height": bot_right_corner.y - top_left_corner.y}

    return monitor

def get_frame(monitor, sct):
    frame = np.array(sct.grab(monitor))
    ## Delete alpha values from array to convert to something usable by OpenCV
    frame = np.delete(frame, 3, axis=2)

    return frame

def load_models():
    fast_model = m.load('../models/keras/experimental_model.keras')
    verification_model = m.load('../models/keras/model.keras')
    m.warm_up(fast_model)
    m.warm_up(verification_model)
    FAST_MODEL_PREDICTION_TIME = m.set_prediction_time(fast_model)
    VERIFICATION_MODEL_PREDICTION_TIME = m.set_prediction_time(verification_model)

    return fast_model, verification_model

def check_reset_run(s, frame, reset_template, curr, rs = False):
    if(template_matching.match_template(frame, reset_template, .6)):
        if((rs == True and curr != 4 and curr != 8 and curr != 12) or (rs == False)):
            ls.reset(s)
            return False

    return True

def KartSplitter64(monitor, fast_model, verification_model, reset_template, console_reset_template, tracks_templates, s):
    ##TODO: Clean up this mess
    recently_split = False
    run = False

    with mss.mss() as sct:
        while True:
            while run:
                frame = get_frame(monitor, sct)
                curr = ls.get_current_split(s)
                ## Check if run has finished
                if(curr == 16):
                    run = False
                    break

                if(recently_split == True and curr != -1):
                    if(template_matching.match_template(frame, tracks_templates[curr], .7)):
                        print("Template match. New track started")
                        recently_split = False
                        time.sleep(10)

                    run = check_reset_run(s, frame, reset_template, curr, True)
                    if run == False:
                        print("Reset run detected")
                        break
                                 
                else:                       
                    ## Check if either run has reset (-1),
                    ## or run has finished (16)
                    if(curr == -1 or curr == 16):
                        run = False
                        break

                    pred = m.predict(frame, fast_model)
                    
                    if(pred[0][0] == 1.0):
                        ## Run verification prediction to confirm results
                        pred = m.predict(frame, verification_model)
                        if(pred[0][0] > 0.9):
                            ls.retroactive_split(s, FAST_MODEL_PREDICTION_TIME + VERIFICATION_MODEL_PREDICTION_TIME)
                            recently_split = True
                            print("Split probs: " + str(pred))

                    run = check_reset_run(s, frame, reset_template, curr)
                    if run == False:
                        print("Reset run detected")
                        break

                    elif(template_matching.match_template(frame, console_reset_template, .01, "TM_SQDIFF_NORMED")):
                        print("Missed split. Applying retroactive split")
                        ls.retroactive_split(s, CONSOLE_RESET_TIME)
                        recently_split = True
                             
            else:
                frame = get_frame(monitor, sct)

                if(template_matching.match_template(frame, tracks_templates[0], .7)):
                    print("Start of run detected")
                    ls.start(s)
                    recently_split = False
                    run = True
                    time.sleep(5)
                    
                cv.waitKey(25)

if __name__ == "__main__":
    fast_model, verification_model = load_models()
    reset_template, console_reset_template = template_matching.load_reset_templates()
    tracks_templates = template_matching.load_track_templates()
    os.system('cls')

    s = ls.connect()
    ls.switch_to_gametime(s)
    monitor = get_capture()

    KartSplitter64(monitor, fast_model, verification_model, reset_template, console_reset_template, tracks_templates, s)
