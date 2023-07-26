from deepface import DeepFace
from flask import Flask, request, Response
from statistics import mode
import cv2
import numpy as np
from pygame import mixer
import threading
import time


global count
global emotion_list
emotion_list=[]
global Commen_emotion
Commen_emotion=""
count=0
global flag
global flag_emotion
flag_emotion=False
flag = False
app = Flask(__name__)

def play_voice(name,name2):
    mixer.init()
    if mixer.music.get_busy():
        mixer.music.stop()
    mixer.music.load(name)
    mixer.music.play(1)
    while mixer.music.get_busy():
        pass
    if name2!=None:
        mixer.music.load(name2)
        mixer.music.play(1)
        while mixer.music.get_busy():
            pass
@app.route('/api/reset', methods=['POST'])
def fl():
    global flag_emotion
    global flag
    flag_emotion=False
    flag=False
    return Response(status=200)
@app.route('/api/test', methods=['POST'])
def test():
    global flag
    if not flag:
        x = threading.Thread(target=play_voice, args=("start1.mp3","start2.mp3",))
        x.start()
        flag = True
    global count
    global emotion_list
    global Commen_emotion
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    count=count+1
    predication=0
    global flag_emotion
    if(not flag_emotion):
        predication=DeepFace.analyze(img,actions = ['emotion'],enforce_detection=False)
        #print(predication)
        #cv2.putText(img,str(predication['dominant_emotion'])+ ": " + str(round(predication['emotion'][predication['dominant_emotion']],2)),(x,y-10),font,1,(0,255,0),2, cv2.LINE_AA)
        emotion_list.append(predication['dominant_emotion'])
        if(len(emotion_list)>10):
            try:
                Commen_emotion=mode(emotion_list)
                flag_emotion=True
                emotion_list=[]
            except:
                pass
        if (Commen_emotion!=""):
            if(Commen_emotion=="happy"):
                mixer.music.stop()
                x = threading.Thread(target=play_voice, args=("Happy.mp3",None))
                x.start()
                Commen_emotion=""
                print("Happy")
            elif(Commen_emotion=="sad"):
                mixer.music.stop()
                x = threading.Thread(target=play_voice, args=("Sad.mp3",None,))
                x.start()
                Commen_emotion=""
                print("Sad")
            elif(Commen_emotion=="angry"):
                mixer.music.stop()
                x = threading.Thread(target=play_voice, args=("Angry.mp3",None,))
                x.start()
                Commen_emotion=""
                print("Sad")
            elif(Commen_emotion=="surprise"):
                mixer.music.stop()
                x = threading.Thread(target=play_voice, args=("Surprise.mp3",None,))
                x.start()
                Commen_emotion=""
                print("Sad")
            elif(Commen_emotion=="neutral"):
                mixer.music.stop()
                x = threading.Thread(target=play_voice, args=("N.mp3",None,))
                x.start()
                Commen_emotion=""
                print("Sad")

    return Response(status=200)
app.run(host="0.0.0.0", port=5000)