from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
import paho.mqtt.client as mqtt
# Create your views here.
def index(req):
    return render(req, 'mainapp/index.html')
@csrf_exempt
def setspeed(request):
    if request.is_ajax():
        if request.method == 'POST':
            client = mqtt.Client()
            client.connect("test.mosquitto.org", 1883, 60)
            topic = 'set_velocity_amirkabir'
            client.publish(topic, payload=request.body.decode())
    return HttpResponse("OK")

@csrf_exempt
def setangularcam(request):
    if request.is_ajax():
        if request.method == 'POST':
            client = mqtt.Client()
            client.connect("test.mosquitto.org", 1883, 60)
            topic = 'set_angularcam_amirkabir'
            client.publish(topic, payload=request.body.decode())
    return HttpResponse("OK")

@csrf_exempt
def lincammov(request):
    if request.is_ajax():
        if request.method == 'POST':
            client = mqtt.Client()
            client.connect("test.mosquitto.org", 1883, 60)
            topic = 'set_lincam_amirkabir'
            client.publish(topic, payload=request.body.decode())
    return HttpResponse("OK")