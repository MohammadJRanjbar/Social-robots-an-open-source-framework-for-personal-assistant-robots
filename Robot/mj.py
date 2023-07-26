#!/usr/bin/env python
import math
from math import sin, cos, pi
import serial
import time
import readchar
import getch
import keyboard
import json
import paho.mqtt.client as mqtt

import requests
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
from flask import Flask, request, Response

global serialport
global data_list
global tmp_value
global data_count
global error_count
global MAX_Speed
global MIN_Speed
global X_pos
global Y_pos
global ang
global V_ang
global V_linear
global last_time
global servo_ang
global MR_speed
global ML_speed
global last_teta
global mode
def init():
    global serialport
    global MAX_Speed
    global MIN_Speed
    global data_list
    global tmp_value
    global X_pos
    global Y_pos
    global ang
    global V_ang
    global V_linear
    global last_time
    global error_count
    global servo_ang
    global MR_speed
    global ML_speed
    global last_teta
    global mode
    MR_speed = "+000"
    ML_speed = "+000"
    last_teta = 0
    servo_ang = str(50)
    MAX_Speed = 20
    MIN_Speed = -20
    serialport = serial.Serial ("/dev/ttyS0")
    serialport.baudrate = 115200
    data_list = []
    tmp_value = ""
    X_pos = 0.0
    Y_pos = 0.0
    ang = 0.0
    V_ang = 0
    V_linear = 0
    error_count =0
    mode = "sleep"

def speed_maker(speed):
    global MAX_Speed
    global MIN_Speed
    if(speed >= MIN_Speed and speed <= MAX_Speed):
        if(speed >= 0):
            digit_10 = int((speed/10)%10)
            digit_1 = int(speed%10)
            digit_01 = int((speed*10)%10)
            result = "+" + str(digit_10) + str(digit_1) + str(digit_01)
        else:
            speed= -1*speed
            digit_10 = int((speed/10)%10)
            digit_1 = int(speed%10)
            digit_01 = int((speed*10)%10)
            result = "-" + str(digit_10) + str(digit_1) + str(digit_01)
            print(result)
    elif(speed < MIN_Speed):
        result = speed_maker(MIN_Speed)
    else:
        result = speed_maker(MAX_Speed)
    return result

def digits_maker(num):
    if(num <10 and num >0):
        digits = str(0) + str(ang)
    elif(num<=0):
        digits = "00"
    elif(num>99):
        digits = "99"
    else:
        digits = str(num)
    return digits


def callback(mr,ml):
    global MR_speed
    global ML_speed
    global servo_ang 
    ML_speed = speed_maker(ml)
    MR_speed = speed_maker(mr)
    data = MR_speed + ML_speed + servo_ang + "+00"
    serialport.write(data.encode())

def linear_camera_callback(t,direct):
    global servo_ang
    global MR_speed
    global ML_speed
    t = digits_maker(t)
    data = MR_speed + ML_speed + servo_ang + direct + t
    serialport.write(data.encode())

def servo_callback(ang):
    global MR_speed
    global ML_speed
    global servo_ang
    servo_ang = digits_maker(ang)
    data = MR_speed + ML_speed + servo_ang + "+00"
    print(data)
    serialport.write(data.encode())



app = Flask(__name__)

@app.route('/api/picovoice', methods=['GET'])
def mode1():
    global mode
    mode_tmp = mode
    if (mode == "sleep"):
        callback(4, -4)
        servo_callback(60)
        mode = "ready"
    return Response(response=mode_tmp, status=200 )

@app.route("/api/face_detect")
def mode_face():
    global mode
    if(mode!="detect"):
        mode = "detect"
        callback(0, 0)
    return Response(status=200)

@app.route('/api/stop', methods=['GET'])
def mode2():
    if mode == "detect":
        callback(0, 0)
    return Response(status=200)

@app.route('/api/go', methods=['GET'])
def mode31():
    if mode == "detect":
        callback(7, 7)
    return Response(status=200 )

@app.route('/api/up', methods=['GET'])
def mode3():
    if mode == "detect":
        servo_callback(70)
    return Response(status=200 )

@app.route('/api/down', methods=['GET'])
def mode4():
    if mode == "detect":
        servo_callback(30)
    return Response(status=200 )

@app.route('/api/left', methods=['GET'])
def mode5():
    if mode == "detect":
        callback(7, -7)
    return Response(status=200 )

@app.route('/api/right', methods=['GET'])
def mode6():
    if mode == "detect":
        callback(-7, 7)
    return Response(status=200 )

@app.route('/api/sleep', methods=['GET'])
def mode7():
    global mode
    if(mode!="ready" and mode!="sleep"):
        callback(0, 0)
        servo_callback(0)
        mode = "sleep"
    return Response(status=200)

if __name__ == '__main__': 
    init()
    print("what up")
    app.run(host="0.0.0.0", port=5000)

    




