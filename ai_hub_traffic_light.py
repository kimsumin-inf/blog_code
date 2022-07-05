import os
import numpy as np
import shutil
import cv2
import json

def convert(size, box):
    # box: x_min,y_min, x_max,y_max
    # size: w, h
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[2])/2.0
    y = (box[1] + box[3])/2.0
    w = box[2] - box[0]
    h = box[3] - box[1]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (str(x),str(y),str(w),str(h))
count =0

IMAGE_PATH = "/home/sumin/Downloads/traffic/Training/c" # Image PATH
LABEL_PATH = "/home/sumin/Downloads/traffic/Training/d" # Label PATH
NEW_LABEL_PATH = "/home/sumin/Downloads/traffic/Training/labels2" # NEW Label PATH
NEW_IMAGE_PATH = "/home/sumin/Downloads/traffic/Training/images2" # NEW Image PATH

IMAGE = sorted(os.listdir(IMAGE_PATH))
LABEL = sorted(os.listdir(LABEL_PATH))

for i in range(len(LABEL)):
    with open(os.path.join(LABEL_PATH,LABEL[i]),'r') as json_file:
        label = json.load(json_file)
    j= i
    if len(label["annotation"])>=1:
        for i in label["annotation"]:

            class_id = None

    if (i["class"]=="traffic_light" and i["type"]=="car" and i["direction"] == "horizontal") :
        if i["light_count"] =="3" or i["light_count"]=="4":
            state = i["attribute"][0]

        if state["x_light"]=="on" or state["others_arrow"] =="on":
            continue

        if state["red"] =="off" and state["green"] =="on" and state["yellow"]=="off" and state["left_arrow"]=="off":
            class_id = "0"
            bbox = i["box"]
            size = label["image"]["imsize"]
            x,y,w,h = convert(size,bbox)

            Str = class_id+' '+x+' '+y+' '+ w + ' '+ h+'\n'

        with open(os.path.join(NEW_LABEL_PATH,LABEL[j].replace(".json",".txt")),'a') as res:
            res.writelines(Str)
            res.close()
        count +=1
    
    elif state["red"] =="on" and state["green"] =="off" and state["yellow"]=="off" and state["left_arrow"]=="off":
        class_id = "1"
        count +=1
        bbox = i["box"]
        size = label["image"]["imsize"]
        x,y,w,h = convert(size,bbox)
        Str = class_id+' '+x+' '+y+' '+ w + ' '+ h+'\n'

        with open(os.path.join(NEW_LABEL_PATH,LABEL[j].replace(".json",".txt")),'a')as res:
            res.writelines(Str)
            res.close()
    
    elif state["red"] =="off" and state["green"] =="on" and state["yellow"]=="off" and state["left_arrow"]=="on":
        class_id = "2"
        count +=1
        bbox = i["box"]
        size = label["image"]["imsize"]
        x,y,w,h = convert(size,bbox)
        Str = class_id+' '+x+' '+y+' '+ w + ' '+ h+'\n'
    
        with open(os.path.join(NEW_LABEL_PATH,LABEL[j].replace(".json",".txt")),'a')as res:
            res.writelines(Str)
            res.close()

    elif state["red"] =="on" and state["green"] =="off" and state["yellow"]=="off" and state["left_arrow"]=="on":
        class_id = "3"
        count +=1
        bbox = i["box"]
        size = label["image"]["imsize"]
        x,y,w,h = convert(size,bbox)
        Str = class_id+' '+x+' '+y+' '+ w + ' '+ h+'\n'
    
        with open(os.path.join(NEW_LABEL_PATH,LABEL[j].replace(".json",".txt")),'a')as res:
            res.writelines(Str)
            res.close()
    
    elif state["red"] =="off" and state["green"] =="off" and state["yellow"]=="on" and state["left_arrow"]=="off":
        class_id = "4"
        count +=1
        bbox = i["box"]
        size = label["image"]["imsize"]
        x,y,w,h = convert(size,bbox)
        Str = class_id+' '+x+' '+y+' '+ w + ' '+ h+'\n'

        with open(os.path.join(NEW_LABEL_PATH,LABEL[j].replace(".json",".txt")),'a')as res:
            res.writelines(Str)
            res.close()
    
    else :
        pass


 
lab =sorted(os.listdir(NEW_LABEL_PATH))
for j in range(len(lab)):
 
    if os.path.isfile(os.path.join(IMAGE_PATH,lab[j].replace(".txt",".jpg"))):
        src = os.path.join(IMAGE_PATH,lab[j].replace(".txt",".jpg"))
        dst = os.path.join(NEW_IMAGE_PATH,lab[j].replace(".txt",".jpg"))
        shutil.move(src,dst)
    
    else:
        print(os.path.join(IMAGE_PATH,lab[j]))
    pass

img = sorted(os.listdir(NEW_LABEL_PATH))
count = 0
for i in range(len(img)):
    if os.path.isfile(os.path.join(NEW_IMAGE_PATH,img[i].replace(".txt",".jpg"))):
        pass
    else:
        os.remove(os.path.join(NEW_LABEL_PATH,img[i]))
        count +=1
print(count)
