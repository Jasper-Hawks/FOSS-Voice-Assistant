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
engine = pyttsx3.init("espeak",True) # Initialize the voice engine from pyttsx3

# These voices are based off of the ones that are installed onto your system
# We're using espeak since we're on Linux

# Notify the user that we are setting up the assistant
engine.say("Setting things up...")

r = sr.Recognizer()
mic = sr.Microphone()
userAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'
headers = {"User-Agent":userAgent}

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

# Run and wait allows the voice assistant to process the commands
# that we give it that involve speaking

def speak():
    request = "" # TODO Rename this because I'll probably use the request library

    with mic as source:

        r.adjust_for_ambient_noise(source)
        print("Say something") # TODO this is being printed later than expected
        audio = r.listen(source)

        try:
            # TODO Switch this back to sphinx when done testing
            request = r.recognize_google(audio)
            understood = True
        except sr.UnknownValueError:
            engine.say("I don't understand, can you please repeat that.")
        except sr.RequestError:
            engine.say("I can not access the API")
        except:
            # TODO Eventually remove this once everything is working
            print("Something went wrong")

    engine.runAndWait()
    return(request)

engine.runAndWait()
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

# TODO Add who when where why and how
if "what" in action or "who" in action or "when" in action or "where" in action or "why" in action or "how" in action:

    # TODO Also find a way to answer more complicated questions like:
    # How do you calculate the hypotenuse of a triangle
    #
    # For now simple questions can be found and answered with tts
    # We'll have to find more complicated questions

    engine.say("Searching for," + action)
    driver = webdriver.Firefox(firefox_profile=profile)

    #TODO Decide whether we want to implement regex or not

    # Search engines generate results using JavaScript
    # so we can not use bs4 and requests in order to
    # scrape duckduckgo with just a http request.
    #
    # Instead we can generate the site with selenium and
    # try to scrape from there

    # Then if they are unavailable we will have to look at
    # summaries of different articles


    driver.get("https://duckduckgo.com/?q=" + action)

    try:
        # Try to find the sidebar wikipedia module
        ans = driver.find_element_by_xpath("/html/body/div[2]/div[5]/div[3]/div/div[2]/div[2]/div/div/div[1]/div/div[2]/span")
    except:
        # If that does not work read the first article on the page
        #
        # Instead of reading the article we can instead do what similar
        # assistants do and just show the user the article since the
        # assistant will also have a GUI.
        # Then say this is what i found

        ans = driver.find_element_by_xpath("/html/body/div[2]/div[5]/div[3]/div/div[1]/div[5]/div[1]/div/div[2]")

    print(ans.text)
    engine.say(ans.text)
    engine.runAndWait()

