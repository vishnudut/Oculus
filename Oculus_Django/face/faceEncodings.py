from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os
import numpy as np


@csrf_exempt
def encoding(request):
    data = request.FILES['user_img']
    name = request.POST['user_name']
    print(name)
    print(data)
    imagebits = data.read()
    print(imagebits)
    uti_formate = np.fromstring(imagebits,np.uint8)
    print(uti_formate)
    img = cv2.imdecode(uti_formate, cv2.IMREAD_COLOR)
    # np_data = np.asarray(uti_formate)
    # print('THIS IS NP DTA:', np_data)
    rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb,model='hog')
    encodings = face_recognition.face_encodings(rgb, boxes)
    print(encodings)            
        
        
    return HttpResponse('Encoding')

    