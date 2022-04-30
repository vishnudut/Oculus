import speech_recognition as sr # recognise speech
import playsound # to play an audio file
from gtts import gTTS # google text to speech
import random
from time import ctime # get time details
import time
import os # to remove created audio files 

from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition

import imutils
import pickle
import time
import cv2

from time import sleep
from ocr import img_to_text



class person:
    name = ''
    def setName(self, name):
        self.name = name

def there_exists(terms):
    for term in terms:
        if term in voice_data:
            return True



def speak(audio_string):
    tts = gTTS(text=audio_string, lang='en') # text to speech(voice)
    r = random.randint(1,20000000)
    audio_file = 'audio' + str(r) + '.mp3'
    tts.save(audio_file) # save as mp3
    playsound.playsound(audio_file) # play the audio file
    print(f"jarvis: {audio_string}") # print what app said
    os.remove(audio_file) # remove audio file


def whoIsThat():
    print("[INFO] loading encodings + face detector...")
    data = pickle.loads(open('encodings.pickle',"rb").read())
    print("what data is",data)
    detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    fps = FPS().start()

    names= []

    for i in range(30):
        frame = vs.read()
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        rects = detector.detectMultiScale(gray, scaleFactor=1.1,
            minNeighbors=5, minSize=(30,30),
            flags=cv2.CASCADE_SCALE_IMAGE)
        
        boxes = [(y,x+w,y+h,x) for (x,y,w,h) in rects]

        encodings = face_recognition.face_encodings(rgb,boxes)

        for encoding in encodings:
            matches = face_recognition.compare_faces(data["encodings"],encoding)
            name = "Unkown"

            if True in matches:
                matchedIdxs = [i for (i,b) in enumerate(matches) if b]
                counts = {}

                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                name = max(counts, key=counts.get)
            names.append(name)

        for ((top, right, bottom, left), name) in zip(boxes, names):
            cv2.rectangle(frame, (left, top), (right, bottom),(0, 255, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

        fps.update()

    fps.stop()
    print("It's ", names[0])
    cv2.destroyAllWindows()
    vs.stop()
    return names

r = sr.Recognizer() # initialise a recogniser
# listen for audio and convert it to text:
def record_audio(ask=False):
    with sr.Microphone() as source: # microphone as source
        if ask:
            speak(ask)
        audio = r.listen(source)  # listen for the audio via source
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)  # convert audio to text
        except sr.UnknownValueError: # error: recognizer does not understand
            speak('I did not get that')
        except sr.RequestError:
            speak('Sorry, the service is down') # error: recognizer is not connected
        print(f">> {voice_data.lower()}") # print what user said
        return voice_data.lower()

# screenshot method
def take_screenshot ():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("screen capture")

    img_counter =0
    while(True):
        ret,frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test",frame)
        k = cv2.waitKey(1)
    # when escape key is hit
        if k%256 == 27:
            print("escape hit")
            break
    # when space bar is hit
        elif k%256 == 32 :
            img_name = "opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(img_name,frame)
            print("screenshot taken")
            img_counter+=1

    cam.release()
    cv2.destroyAllWindows()
    print("filename",img_name)
    img_to_text(img_name)
    return img_name


def respond(voice_data):
    # 1: greeting
    if there_exists(['hey','hi','hello']):
        greetings = [f"hey, how can I help you {person_obj.name}", f"hey, what's up? {person_obj.name}", f"I'm listening {person_obj.name}", f"how can I help you? {person_obj.name}", f"hello {person_obj.name}"]
        greet = greetings[random.randint(0,len(greetings)-1)]
        speak(greet)

    # 2: name
    if there_exists(["what is your name","what's your name","tell me your name"]):
        if person_obj.name:
            speak("my name is jarvis")
        else:
            speak("my name is jarvis. what's your name?")

    if there_exists(["my name is"]):
        person_name = voice_data.split("is")[-1].strip()
        speak(f"okay, i will remember that {person_name}")
        person_obj.setName(person_name) # remember name in person object

    # 3: greeting
    if there_exists(["how are you","how are you doing"]):
        speak(f"I'm very well, thanks for asking {person_obj.name}")

    # 4: time
    if there_exists(["what's the time","tell me the time","what time is it"]):
        time = ctime()
        speak(time)
    # 5 : face recognition
    if there_exists(['who is that']):
        person = whoIsThat()
        response = "It's " + person[0]
        speak(response)
    # take screennshot and capture convert image into text
    if there_exists(["take screenshot"]):
        img_name = take_screenshot()
        speak("press spacebar to take screenshot")
        print(img_name)
        
    # 6 :exit
    if there_exists(["exit", "quit", "goodbye"]):
        speak("going offline")
        exit()


time.sleep(1)

person_obj = person()
print('How can I help you ?')
while(1):
    voice_data = record_audio() # get the voice input
    print(voice_data)
    respond(voice_data) # respond