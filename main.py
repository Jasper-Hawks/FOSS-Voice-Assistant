# This is the main file that will hold the majority
# of the voice assistants functionality

# PROTOTYPE
import speech_recognition as sr # Library that allows us to find 
import pyttsx3  # Library that allows for text to speech
import time # Library that allows us to manipulate time
import requests # Library that allows us to send HTTP requests
from bs4 import BeautifulSoup # Library that allows us to scrape elements from an HTML file

engine = pyttsx3.init() # Initialize the voice engine from pyttsx3

# These voices are based off of the ones that are installed onto your system
# We're using espeak since we're on Linux

engine.say("Setting things up...")

r = sr.Recognizer()
mic = sr.Microphone()

time.sleep(2)

engine.say("I'm Jim how may I help you")

engine.runAndWait()

def speak():
    request = "" # TODO rename this because I'll probably use the request library

    with mic as source:

        r.adjust_for_ambient_noise(source)
        print("Say something")
        audio = r.listen(source)

        try:
            request = r.recognize_sphinx(audio)
        except sr.UnknownValueError:
            print("I don't understand")
        except sr.RequestError:
            print("Error could not access API")
    return(request)

action = speak()

if "play" in action:
    
    # We're going to have to get some sort of media player
    # I'm leaning towards vlc
    req = requests.get(
