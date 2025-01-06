import cv2 as cv
import os

def load_track_templates():
    tracks_dict =   {'lr' : 0, 'mmf' : 1, 'ktb' : 2, 'kd' : 3, 'tt' : 4,
                    'fs' : 5, 'cm' : 6, 'mr' : 7, 'ws' : 8, 'sl' : 9, 
                    'rry' : 10, 'bc' : 11, 'dkjp' : 12, 'yv' : 13, 
                    'bb' : 14, 'rrd' : 15}
    
    assets_dir = "../templates/tracks"
    list = os.listdir(assets_dir)
    tracks_templates = {}
        
    for img in list:
        track_template = cv.imread(os.path.join(assets_dir, img))
        track_template = cv.resize(track_template, (200, 200))
        track_number = tracks_dict[img.split('.')[0]]
        tracks_templates[track_number] = track_template

    return tracks_templates

def load_reset_templates():
    reset_template = cv.imread("../templates/misc/reset.png")
    reset_template = cv.resize(reset_template, (200, 200))
    console_reset_template = cv.imread("../templates/misc/console_reset.png")
    console_reset_template = cv.resize(console_reset_template, (200, 200))

    return reset_template, console_reset_template

def match_template(frame, template, threshold=0.8, m="TM_CCOEFF_NORMED"):
    method = getattr(cv, m)
    frame = cv.resize(frame, (200,200))
    res = cv.matchTemplate(frame, template, method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

    if(m == "TM_SQDIFF" or m == "TM_SQDIFF_NORMED"):
        if(min_val < threshold):
            return True     
    else:
        if(max_val > threshold):
            return True

    return False

    


    
