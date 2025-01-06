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

MODEL_PREDICTION_TIME = 0
CONSOLE_RESET_TIME = 2700

def KartSplitter64():

    ##TODO: Clean up this mess
    model = m.load('../models/keras/model.keras')
    m.warm_up(model)
    MODEL_PREDICTION_TIME = m.set_prediction_time(model)
    reset_template, console_reset_template = template_matching.load_reset_templates()
    tracks_templates = template_matching.load_track_templates()

    os.system('cls')
    s = ls.connect()
    ls.switch_to_gametime(s)

    input("Move mouse to top left corner of captured video, then press enter:")
    top_left_corner = pyautogui.position()
    input("Move mouse to bottom right corner of captured video, then press enter:")
    bot_right_corner = pyautogui.position()

    monitor = {"top": top_left_corner.y, "left": top_left_corner.x, "width": bot_right_corner.x - top_left_corner.x, "height": bot_right_corner.y - top_left_corner.y}
    recently_split = False
    run = False

    with mss.mss() as sct:
        while True:
            while run:
                frame = np.array(sct.grab(monitor))
                frame = np.delete(frame, 3, axis=2)

                curr = ls.get_current_split(s)

                if(curr == 16):
                    run = False
                    recently_split = False
                    break

                if(recently_split == True and curr != -1):
                    
                    if(template_matching.match_template(frame, tracks_templates[ls.get_current_split(s)], .7)):
                        print("Template match. New track started")
                        recently_split = False
                        time.sleep(10)
                    elif(template_matching.match_template(frame, reset_template, .6) and curr != 4 and curr != 8 and curr != 12):
                        recently_split = False
                        run = False
                        ls.reset(s)
                        break
                                 
                else:                       
                    ##Check if either run has reset (-1),
                    ##or run has finished (16)
                    if(curr == -1 or curr == 16):
                        run = False
                        break

                    pred = m.predict(frame, model)
                    
                    if(pred[0][0] > 0.9):
                        print("Split probs: " + str(pred))
                        recently_split = True
                        ls.retroactive_split(s, MODEL_PREDICTION_TIME)

                    elif(template_matching.match_template(frame, reset_template, .6)):
                        recently_split = False
                        run = False
                        ls.reset(s)
                        break

                    elif(template_matching.match_template(frame, console_reset_template, .01, "TM_SQDIFF_NORMED")):
                        print("Missed split. Applying retroactive split")
                        ls.retroactive_split(s, CONSOLE_RESET_TIME)
                        recently_split = True
                                          
            else:
                frame = np.array(sct.grab(monitor))
                frame = np.delete(frame, 3, axis=2)

                if(template_matching.match_template(frame, tracks_templates[0], .7)):
                    print("Start of run detected")
                    ls.start(s)
                    recently_split = False
                    run = True
                    time.sleep(5)
                    
                cv.waitKey(30)

if __name__ == "__main__":
    KartSplitter64()
