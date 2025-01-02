import cv2 as cv
import numpy as np
import mss as mss
import time
import os
import pyautogui
import socket
from keras.models import load_model
from keras.applications.resnet50 import preprocess_input
from lib.livesplit import start_run, reset_run, split, get_current_split, setup_timer, retroactive_split

def check_template(frame, template, threshold=0.8):
    frame = cv.resize(frame, (200,200))
    res = cv.matchTemplate(frame, template, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

    if(max_val > threshold):
        return True
        
    else: return False

def KartSplitter64():

    ##TODO: Clean up this mess
    
    model = load_model('models/keras/model.keras')
    player_select_template = cv.imread("templates/misc/reset.png")
    player_select_template = cv.resize(player_select_template, (200, 200))
    console_reset_template = cv.imread("templates/misc/console_reset.png")
    console_reset_template = cv.resize(console_reset_template, (200, 200))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 16834))
    setup_timer(s)

    assets_dir = "templates/tracks"
    list = os.listdir(assets_dir)
    tracks_dict = {'lr' : 0, 'mmf' : 1, 'ktb' : 2, 'kd' : 3, 'tt' : 4, 'fs' : 5, 'cm' : 6, 'mr' : 7, 'ws' : 8, 'sl' : 9, 'rry' : 10, 'bc' : 11, 'dkjp' : 12, 'yv' : 13, 'bb' : 14, 'rrd' : 15}
    tracks_templates = {}
        
    for img in list:
        track_template = cv.imread(os.path.join(assets_dir, img))
        track_template = cv.resize(track_template, (200, 200))
        track_number = tracks_dict[img.split('.')[0]]
        tracks_templates[track_number] = track_template
        
    input("Move mouse to top left corner of captured video, then press enter")
    top_left_corner = pyautogui.position()
    input("Move mouse to bottom right corner of captured video, then press enter")
    bot_right_corner = pyautogui.position()

    monitor = {"top": top_left_corner.y, "left": top_left_corner.x, "width": bot_right_corner.x - top_left_corner.x, "height": bot_right_corner.y - top_left_corner.y}
    recently_split = False
    run = False

    with mss.mss() as sct:
        while True:
            while run:
                frame = np.array(sct.grab(monitor))
                frame = np.delete(frame, 3, axis=2)

                curr = get_current_split(s)

                if(curr == 16):
                    run = False
                    recently_split = False
                    break

                if(recently_split == True and curr != -1):
                    
                    if(check_template(frame, tracks_templates[get_current_split(s)])):
                        recently_split = False
                        time.sleep(10)
                    elif(check_template(frame, player_select_template, .6) and curr != 4 and curr != 8 and curr != 12):
                        recently_split = False
                        run = False
                        reset_run(s)
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
                        print(pred)
                        recently_split = True
                        filename = str(pred) + ".jpg"
                        cv.imwrite(os.path.join("testing-screenshots", filename), frame)
                        split(s)

                    elif(check_template(frame, player_select_template, .6)):
                        recently_split = False
                        run = False
                        reset_run(s)
                        break

                    elif(check_template(frame, console_reset_template, .7)):
                        retroactive_split(s)
                        recently_split = True
                                          
                    cv.waitKey(15)
            else:
                frame = np.array(sct.grab(monitor))
                frame = np.delete(frame, 3, axis=2)

                if(check_template(frame, tracks_templates[0], .8)):
                    start_run(s)
                    run = True
                    time.sleep(5)
                    
                cv.waitKey(15)

if __name__ == "__main__":
    KartSplitter64()
