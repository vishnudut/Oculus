from django.shortcuts import render
from django.http import HttpResponse

from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os



def encoding(request):
    data = request.FILES['encoding']
    name = request.data['name']
    print(data)
    print(name)


    