
import cv2
import requests
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
addr = 'http://192.168.145.169:8080'
test_url = addr + '/api/face_detection'

# prepare headers for http request
content_type = 'image/jpeg'
headers = {'content-type': content_type}
#cap = cv2.VideoCapture(0)
camera = PiCamera()
#camera.resolution = (320, 240)
#camera.framerate = 32
rawCapture = PiRGBArray(camera)
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    try:
        c,frm = cv2.imencode('.JPEG', frame.array)
        #data = (frm.tobytes())
        requests.post(test_url, data=frm.tostring(), headers=headers)
        rawCapture.truncate(0)
        #time.sleep(.35)
    except Exception as e:
        rawCapture.truncate(0)
        print(e)