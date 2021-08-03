# This is the main file that will hold the majority
# of the voice assistants functionality

# TODO Eventually create a GUI interface akin to Suri

# PROTOTYPE
import speech_recognition as sr # Library that allows us to find
import pyttsx3  # Library that allows for text to speech
import time # Library that allows us to manipulate time
import requests # Library that allows us to send HTTP requests
import re # Regex library for manipulating strings
from selenium import webdriver
from bs4 import BeautifulSoup # Library that allows us to scrape elements from an HTML file

#TODO Find a way to change the driver to espeak
engine = pyttsx3.init() # Initialize the voice engine from pyttsx3

# These voices are based off of the ones that are installed onto your system
# We're using espeak since we're on Linux

# Notify the user that we are setting up the assistant
engine.say("Setting things up...")

r = sr.Recognizer()
mic = sr.Microphone()


# TODO Fix adding extensions to geckodriver
profile = webdriver.FirefoxProfile()
uB = "./uBlock.xpi"
profile.add_extension(extension=uB)

time.sleep(2)

# TODO Eventually we will have to create a dedicated setup
# where you can rename the assistant and set other preferences
# for now we'll have a placeholder name, Jim, and cross that
# line when we get to it

engine.say("I'm Jim how may I help you")

# Run and wait allows the voice assistant to wait for anymore commands
# that we give it that involve speaking
engine.runAndWait()

def speak():
    request = "" # TODO Rename this because I'll probably use the request library

    with mic as source:

        r.adjust_for_ambient_noise(source)
        print("Say something")
        audio = r.listen(source)

        try:
            # TODO Switch this back to sphinx when done testing
            request = r.recognize_google(audio)
        except sr.UnknownValueError:
            print("I don't understand")
        except sr.RequestError:
            print("Error could not access API")
        except:
            # TODO Eventually remove this once everything is working
            print("Something went wrong")

    return(request)

action = speak()

print(action)

# TODO Come back to the development of play
if "play" in action:

    # We're going to have to get some sort of media player
    # I'm leaning towards vlc

    # TODO check if play is empty or not
    driver = webdriver.Firefox(firefox_profile=profile)

    playPattern = re.compile(".*Play.",re.IGNORECASE)
    search = re.sub(playPattern,"",action)
    engine.say("Now playing: " +search)
    search = re.sub("\s","+",search)

#   req = requests.get("https://www.youtube.com/results?search_query=" + search,headers=headers).text
#   print("https://www.youtube.com/results?search_query=" + search)

    driver.get("https://www.youtube.com/results?search_query=" + search)

    vid = driver.find_element_by_xpath("//*[@id=\"img\"]")
    vid.click()

    # TODO Implement a way to stop the video when it is done


    # Since Youtube doesn't have any structured way of making the URLS
    # of videos we'll have to take our first guess

    # If we want we can separate requests between music and videos and have Spotify
    # handle music while we deal with videos on Youtube
#   soup = BeautifulSoup(req,"html.parser")
#   print(soup.prettify())

#   for link in soup.find_all("div", class_ = "style-scope ytd-section-list-renderer"):
#       print("ran")
#       print(link)

if "what" in action:

    driver = webdriver.Firefox(firefox_profile=profile)

    #TODO Decide whether we want to implement regex or not





