import cv2 as cv
import numpy as np
import mss as mss
import time
import os
import pyautogui
from keras.models import load_model
from keras.applications.resnet50 import preprocess_input
import lib.livesplit as ls
import template_matching

def KartSplitter64():

    ##TODO: Clean up this mess

    model = load_model('models/keras/model.keras')
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
                    
                    if(template_matching.match_template(frame, tracks_templates[ls.get_current_split(s)])):
                        print("Template match. New track started")
                        recently_split = False
                        time.sleep(10)
                    elif(template_matching.match_template(frame, reset_template, .6) and curr != 4 and curr != 8 and curr != 12):
                        recently_split = False
                        run = False
                        ls.reset(s)
                        break
                        
                    cv.waitKey(15)
                    
                else:                       
                    ##Check if either run has reset (-1),
                    ##or run has finished (16)
                    if(curr == -1 or curr == 16):
                        run = False
                        break

                    validation = np.stack([preprocess_input(cv.resize(frame, (224, 224)))])
                    pred = model.predict(validation, verbose=0)
                    
                    if(pred[0][0] > 0.9):
                        print("Split probs: " + str(pred))
                        recently_split = True
                        filename = str(pred) + ".jpg"
                        cv.imwrite(os.path.join("testing-screenshots", filename), frame)
                        ls.split(s)

                    elif(template_matching.match_template(frame, reset_template, .6)):
                        recently_split = False
                        run = False
                        ls.reset(s)
                        break

                    elif(template_matching.match_template(frame, console_reset_template, .01, "TM_SQDIFF_NORMED")):
                        print("Missed split. Applying retroactive split")
                        ls.retroactive_split(s)
                        recently_split = True
                                          
                    cv.waitKey(15)
            else:
                frame = np.array(sct.grab(monitor))
                frame = np.delete(frame, 3, axis=2)

                if(template_matching.match_template(frame, tracks_templates[0], .8)):
                    print("Start of run detected")
                    ls.start(s)
                    run = True
                    time.sleep(5)
                    
                cv.waitKey(30)

if __name__ == "__main__":
    KartSplitter64()
