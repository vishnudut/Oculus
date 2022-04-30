import speech_recognition as sr # recognise speech
import playsound # to play an audio file
from gtts import gTTS # google text to speech
import random
from time import ctime # get time details
# import webbrowser # open browser
# import ssl
# import certifi
import time
import os # to remove created audio files
# import wikipedia
# from newsapi import NewsApiClient
import pyttsx3

# import pprint
# import requests 

# For playing music using spotify
# import spotipy
# from spotipy.oauth2 import SpotifyOAuth
# from pprint import pprint
from time import sleep
# import spotipy.util as util


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
    print('jarvis: '+audio_string) # print what app said
    os.remove(audio_file) # remove audio file


# def get_weather():
#     api_address='http://api.openweathermap.org/data/2.5/weather?appid=74c70cbf155ba874808f72c02696bad9&q='
#     city = 'Chennai'
#     url = api_address + city
#     json_data = requests.get(url).json()
#     format_add = json_data['weather'][0]['description'];
#     current_temp = json_data['main']['temp']
#     temp_c = current_temp - 273.15
#     temp_c_str = str(int(temp_c)) + ' degree Celsius '
#     print(temp_c)
#     print(format_add)
#     return format_add, temp_c_str


# def get_news():
#     url = 'https://newsapi.org/v2/everything?'
#     news_api = '2689061e28344f46bde8a8dbcfdb119b'
#     parameters = {
#         'q': 'big data', # query phrase
#         'pageSize': 20,  # maximum is 100
#         'apiKey': news_api # your own API key
#     }

#     response = requests.get(url, params=parameters)
#     # Convert the response to JSON format and pretty print it
#     response_json = response.json()
#     # pprint.pprint(response_json)
#     news = ''
#     for i in response_json['articles']:
#         news= news + i['title']
    
#     return news


#Function for playing music

# def play_song():
#     util.prompt_for_user_token('Oculus',
#                            'streaming',
#                            client_id='4876797530b244f1888967346b4ce1fd',
#                            client_secret='235a3ef81629464e8d75e1c57b5f4d65',
#                            redirect_uri='https://open.spotify.com/track/5JKU2tXiG3yvJtefNwe7ZQ')

#     scope = "user-read-playback-state,user-modify-playback-state"
#     sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))
#     # Shows playing devices
#     res = sp.devices()
#     print(res)
#     # Change track
#     sp.start_playback(uris=['spotify:track:6gdLoMygLsgktydTQ71b15'])
#     # Change volume
#     sp.volume(100)

def whoIsThat():
    print("[INFO] loading encodings + face detector...")
    data = pickle.loads(open('encodings.pickle',"rb").read())
    #print(data)
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
print("what is r",r)
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
        print(">> "+voice_data.lower()) # print what user said
        return voice_data.lower()

# get string and make a audio file to be played

# def talk(audio_string):
#     try:
#         something = pyttsx3.init()
#         something.setProperty('rate', 160)
#         something.say(audio_string)
#         something.runAndWait()
#     except Exception as e :
#         print(e)



def respond(voice_data):
    # 1: greeting
    if there_exists(['hey','hi','hello']):
        greetings = ["hey, how can I help you {person_obj.name}", "hey, what's up? {person_obj.name}", "I'm listening {person_obj.name}", "how can I help you? {person_obj.name}", "hello {person_obj.name}"]
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
        # if time[0] == "00":
        #     hours = '12'
        # else:
        #     hours = time[0]
        # minutes = time[1]
        # time = f'{hours} {minutes}'
        speak(time)

    # 5: search google
    # if there_exists(["search for"]) and 'youtube' not in voice_data:
    #     search_term = voice_data.split("for")[-1]
    #     url = f"https://google.com/search?q={search_term}"
    #     webbrowser.get().open(url)
    #     speak(f'Here is what I found for {search_term} on google')

    # 6: search youtube
    # if there_exists(["youtube"]):
    #     search_term = voice_data.split("for")[-1]
    #     url = f"https://www.youtube.com/results?search_query={search_term}"
    #     webbrowser.get().open(url)
    #     speak(f'Here is what I found for {search_term} on youtube')

    # if there_exists(["game"]):
    #     voice_data = record_audio("choose among rock paper or scissor")
    #     moves=["rock", "paper", "scissor"]
    
    #     cmove=random.choice(moves)
    #     pmove=voice_data
        

    #     speak("The computer chose " + cmove)
    #     speak("You chose " + pmove)
    #     if pmove==cmove:
    #         speak("the match is draw")
    #     elif pmove== "rock" and cmove== "scissor":
    #         speak("Player wins")
    #     elif pmove== "rock" and cmove== "paper":
    #         speak("Computer wins")
    #     elif pmove== "paper" and cmove== "rock":
    #         speak("Player wins")
    #     elif pmove== "paper" and cmove== "scissor":
    #         speak("Computer wins")
    #     elif pmove== "scissor" and cmove== "paper":
    #         speak("Player wins")
    #     elif pmove== "scissor" and cmove== "rock":
    #         speak("Computer wins")


    # if there_exists(["what is"]):
    #     text = record_audio("What do you need the definition of")
    #     wiki = wikipedia.summary(text, sentences=2)
    #     speak('here is what i found' +wiki)

    
    # if there_exists(["news","what's the news","read the news","what is the news","read news"]):
    #     news = get_news()
    #     print(news)
    #     speak(news)

    # if there_exists(["what's the weather today","weather","today's weather"]):
    #     weather = get_weather()
    #     print(weather[0])
    #     speak(f'According the weather report it will be {weather[0]} and the temprature is {weather[1]}')
        
    # if there_exists(['play song','song','play music']):
    #     print('Playing songs from your playlist...')
    #     play_song()


    if there_exists(["exit", "quit", "goodbye"]):
        speak("going offline")
        exit()


time.sleep(1)

person_obj = person()
print('How can I help you ?')
while(1):
    voice_data = record_audio() # get the voice input
    respond(voice_data) # respond