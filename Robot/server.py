from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2
import socketio
import time
import cv2
from deepface import DeepFace
from statistics import mode
import os
import threading
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer
import time
from os import listdir
from os.path import isfile, join
import random
import pyaudio
import struct
import pyautogui  # to press a button to play the game
import pvporcupine
import os
global is_any_song_played
is_any_song_played=False
global playsong_voice
global stopsong_voice
stopsong_voice=False
playsong_voice=False
global Question_flag
Question_flag=False
mixer.init()
def player(Emotion,flag):

    if(flag):
        listoffiles=os.getcwd()+ "\\" + Emotion
        print(listoffiles)
        onlyfiles = [f for f in listdir(listoffiles) if isfile(join(listoffiles, f))] 
        Songadress=listoffiles+ "\\" + random.choice(onlyfiles)
        # Starting the mixer
    
        # Loading the song
        mixer.music.load(Songadress)

        # Setting the volume
        mixer.music.set_volume(0.6)

        # Start playing the song
        mixer.music.play(-1)
        return True
    else:
        mixer.music.stop()
        return False

key1 = r'stop-the-song__en_windows_2021-11-09-utc_v1_9_0.ppn'
key2 = r'play-a-song__en_windows_2021-11-09-utc_v1_9_0.ppn'
# this is the library path
library_path = os.getcwd()
library_path= library_path + '\Porcupine\lib\windows\\amd64\libpv_porcupine.dll'

# this is model file path can be find inside Porcupine -> lib -> common
model_file_path = r'Porcupine\lib\common\porcupine_params.pv'
keyword_file_paths = [key1,key2]
sensitivities = [1,1]
handle = pvporcupine.Porcupine(library_path, model_file_path, keyword_file_paths=keyword_file_paths, sensitivities=sensitivities)

def get_next_audio_frame():
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(rate=handle.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=handle.frame_length,input_device_index=None)
    pcm = audio_stream.read(handle.frame_length)
    pcm = struct.unpack_from("h" * handle.frame_length, pcm)
    return pcm
 
#in this while if any of those world is going to be audible the code will press the right button 
def thread_voice():
    global playsong_voice
    global stopsong_voice
    while True:
        pcm = get_next_audio_frame()
        keyword_index = handle.process(pcm)
        if keyword_index==0:
            playsong_voice=False
            stopsong_voice=True
            print("Stop")
        elif keyword_index==1:
            playsong_voice=True
            stopsong_voice=False
            print("Play")

def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img
# Initialize the Flask application
app = Flask(__name__)
sio = socketio.Client()
sio.connect('http://127.0.0.1:7000',wait_timeout=20)
global count
global emotion_list
emotion_list=[]
global Commen_emotion
Commen_emotion=""
count=0
x = threading.Thread(target=thread_voice, args=())
x.start()
# route http posts to this method
@app.route('/api/test', methods=['POST'])
def test():
    global count
    global emotion_list
    global Commen_emotion
    global is_any_song_played
    global playsong_voice
    global stopsong_voice
    global Question_flag
    r = request
    facecascade=cv2.CascadeClassifier(cv2.data.haarcascades+ "haarcascade_frontalface_default.xml")
    font=cv2.FONT_HERSHEY_SIMPLEX
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    #imageshow=img.copy()
    #img = cv2.GaussianBlur(img,(3,3),0)
    #img = cv2.resize(img, (640, 480))
    #img = increase_brightness(img, value=30)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=facecascade.detectMultiScale(gray,1.1,4)
    dominant_emotion=""
    dominant_emotion_Percent=0
    count=count+1
    predication=0
    response={}
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        
        
        #print(len(faces))
        predication=DeepFace.analyze(img[y:y+h,x:x+w],actions = ['emotion'],enforce_detection=False)
        #print(predication)
        cv2.putText(img,str(predication['dominant_emotion'])+ ": " + str(round(predication['emotion'][predication['dominant_emotion']],2)),(x,y-10),font,1,(0,255,0),2, cv2.LINE_AA)
        emotion_list.append(predication['dominant_emotion'])
        response['dominant_emotion']=""
    if(len(emotion_list)>21):
        try:
            Commen_emotion=mode(emotion_list)
            response['dominant_emotion']=Commen_emotion
            emotion_list=[]
        except:
            pass
    if (Commen_emotion!=""):
        #print(stopsong_voice)
        if (is_any_song_played==False):
            if(Question_flag==False and Commen_emotion=="sad"):
                mixer.music.load("Sarres.mp3")
                mixer.music.set_volume(0.6)
                # Start playing the song
                mixer.music.play(0)
                Question_flag=True
            
            if(playsong_voice):
                if(Commen_emotion=="happy" or Commen_emotion=="angry" or Commen_emotion=="sad"):
                    is_any_song_played=player(Commen_emotion,True)
                    song_started=True
                    playsong_voice=False
        elif(stopsong_voice):
            is_any_song_played=player("Happy",False)
            stopsong_voice=False
            playsong_voice=False
            song_started=False
            #print("Lower one")
            #print(playsong_voice)
        else:
            pass
            #print(playsong_voice)
            #print("already playing")    #print(len(emotion_list))
    cv2.putText(img,str(Commen_emotion),(140,40),font,1,(0,255,0),2, cv2.LINE_AA)
    #cv2.imshow("test",img)
    response['result']=str(len(faces))
    # do some fancy processing here....

    if(count==1):
        try:
            c,frm = cv2.imencode('.JPEG', img)
            data = (frm.tobytes())
            sio.emit('data',data)
            #rawCapture.truncate(0)
            #time.sleep(.35)
            count=0
        except Exception as e:
            #rawCapture.truncate(0)
            print(e)
            count=0
            #time.sleep(1)
            #sio.connect('http://45.149.77.212:5000')
        # build a response dict to send back to client
    #response = {'result': '{} face detected'.format(len(faces))}
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")


# start flask app
app.run(host="0.0.0.0", port=5000)