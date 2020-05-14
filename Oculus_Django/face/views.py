from django.shortcuts import render
from django.http import HttpResponse
from .models import faceEncodings

from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2
import json

# Create your views here.

detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')



def compareFaces(request):
    db_encodings = faceEncodings.objects.values_list('encodings', flat=True)
    dbEncoded_username = list(faceEncodings.objects.values_list('user_name', flat=True))
    user_encodings = []

    for encoding in db_encodings:
        json_to_list = json.loads(encoding)
        user_encodings.append(json_to_list)

    print(db_encodings)
    print(dbEncoded_username)
    print(user_encodings)

    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    fps = FPS().start()
    print(detector)

    for i in range(90):
        frame = vs.read()
        frame = imutils.resize(frame, width = 500)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # compute the facial embeddings for each face bounding box
        encodings = face_recognition.face_encodings(rgb)
        names = []

        for encoding in encodings:
            matches = face_recognition.compare_faces(user_encodings,
			encoding)
            name = "Unknown"

        if True in matches:
			# find the indexes of all matched faces then initialize a
			# dictionary to count the total number of times each face
			# was matched
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

			# loop over the matched indexes and maintain a count for
			# each recognized face face
            for i in matchedIdxs:
                name = dbEncoded_username[i]
                counts[name] = counts.get(name, 0) + 1

            name = max(counts, key=counts.get)
		# update the list of names
        names.append(name)
        print(names)

    return HttpResponse('This should return the face of the person infront of the camera')
