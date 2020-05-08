import speech_recognition as sr # recognise speech
import playsound # to play an audio file
from gtts import gTTS # google text to speech
import random
from time import ctime # get time details
import webbrowser # open browser
import ssl
import certifi
import time
import os # to remove created audio files
import wikipedia
from newsapi import NewsApiClient

import pprint
import requests 



class person:
    name = ''
    def setName(self, name):
        self.name = name

def there_exists(terms):
    for term in terms:
        if term in voice_data:
            return True

def get_weather():
    api_address='http://api.openweathermap.org/data/2.5/weather?appid=74c70cbf155ba874808f72c02696bad9&q='
    city = 'Chennai'
    url = api_address + city
    json_data = requests.get(url).json()
    format_add = json_data['weather'][0]['description'];
    current_temp = json_data['main']['temp']
    temp_c = current_temp - 273.15
    temp_c_str = str(int(temp_c)) + ' degree Celsius '
    print(temp_c)
    print(format_add)
    return format_add, temp_c_str


def get_news():
    url = 'https://newsapi.org/v2/everything?'
    news_api = '2689061e28344f46bde8a8dbcfdb119b'
    parameters = {
        'q': 'big data', # query phrase
        'pageSize': 20,  # maximum is 100
        'apiKey': news_api # your own API key
    }

    response = requests.get(url, params=parameters)
    # Convert the response to JSON format and pretty print it
    response_json = response.json()
    # pprint.pprint(response_json)
    news = ''
    for i in response_json['articles']:
        news= news + i['title']
    
    return news




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

# get string and make a audio file to be played
def speak(audio_string):
    tts = gTTS(text=audio_string, lang='en') # text to speech(voice)
    r = random.randint(1,20000000)
    audio_file = 'audio' + str(r) + '.mp3'
    tts.save(audio_file) # save as mp3
    playsound.playsound(audio_file) # play the audio file
    print(f"jarvis: {audio_string}") # print what app said
    os.remove(audio_file) # remove audio file

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
        # if time[0] == "00":
        #     hours = '12'
        # else:
        #     hours = time[0]
        # minutes = time[1]
        # time = f'{hours} {minutes}'
        speak(time)

    # 5: search google
    if there_exists(["search for"]) and 'youtube' not in voice_data:
        search_term = voice_data.split("for")[-1]
        url = f"https://google.com/search?q={search_term}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search_term} on google')

    # 6: search youtube
    if there_exists(["youtube"]):
        search_term = voice_data.split("for")[-1]
        url = f"https://www.youtube.com/results?search_query={search_term}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search_term} on youtube')

    if there_exists(["game"]):
        voice_data = record_audio("choose among rock paper or scissor")
        moves=["rock", "paper", "scissor"]
    
        cmove=random.choice(moves)
        pmove=voice_data
        

        speak("The computer chose " + cmove)
        speak("You chose " + pmove)
        if pmove==cmove:
            speak("the match is draw")
        elif pmove== "rock" and cmove== "scissor":
            speak("Player wins")
        elif pmove== "rock" and cmove== "paper":
            speak("Computer wins")
        elif pmove== "paper" and cmove== "rock":
            speak("Player wins")
        elif pmove== "paper" and cmove== "scissor":
            speak("Computer wins")
        elif pmove== "scissor" and cmove== "paper":
            speak("Player wins")
        elif pmove== "scissor" and cmove== "rock":
            speak("Computer wins")


    if there_exists(["what is"]):
        text = record_audio("What do you need the definition of")
        wiki = wikipedia.summary(text, sentences=2)
        speak('here is what i found' +wiki)

    
    if there_exists(["news","what's the news","read the news","what is the news","read news"]):
        news = get_news()
        speak(news)

    if there_exists(["what's the weather today","weather","today's weather"]):
        weather = get_weather()
        print(weather[0])
        speak(f'According the weather report it will be {weather[0]} and the temprature is {weather[1]}')
        

    if there_exists(["exit", "quit", "goodbye"]):
        speak("going offline")
        exit()


time.sleep(1)

person_obj = person()
while(1):
    voice_data = record_audio() # get the voice input
    respond(voice_data) # respond