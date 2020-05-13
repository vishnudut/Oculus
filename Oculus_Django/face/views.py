from django.shortcuts import render
from django.http import HttpResponse


from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2

# Create your views here.

detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')



def compareFaces(request):
    print("[INFO] starting video stream...")
    #vs = VideoStream(src=0).start()
    time.sleep(2.0)
    fps = FPS().start()
    print(detector)
    return HttpResponse('This should return the face of the person infront of the camera')
