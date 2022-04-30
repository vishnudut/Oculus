# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2
# import pyttsx3 as pt
from gtts import gTTS
import os
import playsound
import random

# ap = argparse.ArgumentParser()
# # ap.add_argument("-c", "--cascade", required=True,
# # 	help = "path to where the face cascade resides")
# ap.add_argument("-e", "--encodings", required=True,
# 	help="path to serialized db of facial encodings")
# args = vars(ap.parse_args())

def speak(audio_string):
		tts = gTTS(text=audio_string, lang='en')
		r = random.randint(1,100000000)
		audio_file = 'audio-' + str(r) + '.mp3'
		tts.save(audio_file)
		playsound.playsound(audio_file)
		print(audio_string)
		os.remove(audio_file)


def whoIsThat():
	print("[INFO] loading encodings + face detector...")
	data = pickle.loads(open('encodings.pickle', "rb").read())
	print(data)
	detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	print(detector)

	# initialize the video stream and allow the camera sensor to warm up
	print("[INFO] starting video stream...")
	vs = VideoStream(src=0).start()
	time.sleep(2.0)
	fps = FPS().start()

	names = []

	# loop over frames from the video file stream
	for i in range(60):
		frame = vs.read()
		frame = imutils.resize(frame, width=500)
		
		# convert the input frame from (1) BGR to grayscale (for face
		# detection) and (2) from BGR to RGB (for face recognition)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

		# detect faces in the grayscale frame
		rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
			minNeighbors=5, minSize=(30, 30),
			flags=cv2.CASCADE_SCALE_IMAGE)

		boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
		

		# compute the facial embeddings for each face bounding box
		encodings = face_recognition.face_encodings(rgb, boxes)
		

		# loop over the facial embeddings
		for encoding in encodings:
			matches = face_recognition.compare_faces(data["encodings"],
				encoding)
			name = "Unknown"

			# check to see if we have found a match
			if True in matches:
				# find the indexes of all matched faces then initialize a
				# dictionary to count the total number of times each face
				# was matched
				matchedIdxs = [i for (i, b) in enumerate(matches) if b]
				counts = {}

				# loop over the matched indexes and maintain a count for
				# each recognized face face
				for i in matchedIdxs:
					name = data["names"][i]
					counts[name] = counts.get(name, 0) + 1

				name = max(counts, key=counts.get)
			# update the list of names
			names.append(name)

		# loop over the recognized faces
		for ((top, right, bottom, left), name) in zip(boxes, names):
			# draw the predicted face name on the image
			cv2.rectangle(frame, (left, top), (right, bottom),
				(0, 255, 0), 2)
			y = top - 15 if top - 15 > 15 else top + 15
			cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
				0.75, (0, 255, 0), 2)

		# display the image to our screen
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
		#to print the names

		if key == ord("q"):
			break

		# update the FPS counter
		fps.update()


	fps.stop()
	print("It's ", names[0])
	print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
	print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
	cv2.destroyAllWindows()
	vs.stop()
