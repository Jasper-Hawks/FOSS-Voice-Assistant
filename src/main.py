# This is the main file that will hold the majority
# of the voice assistants functionality

# TODO Eventually create a GUI interface akin to Suri

# PROTOTYPE
import mpv
import mpvListener
import pafy
import speech_recognition as sr # Library that allows us to find
import pyttsx3  # Library that allows for text to speech
import time # Library that allows us to manipulate time
import requests # Library that allows us to send HTTP requests
import re # Regex library for manipulating strings
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup # Library that allows us to scrape elements from an HTML file

#TODO Find a way to change the driver to espeak
engine = pyttsx3.init("espeak",True) # Initialize the voice engine from pyttsx3

# These voices are based off of the ones that are installed onto your system
# We're using espeak since we're on Linux and I'll eventually run this on a
# raspberry pi

# Notify the user that we are setting up the assistant
engine.say("Setting things up...")

r = sr.Recognizer()
r.energy_threshold = 4000
mic = sr.Microphone()
userAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'
headers = {"User-Agent":userAgent}

# TODO Fix adding extensions to geckodriver
profile = webdriver.FirefoxProfile()
profile.add_extension()

time.sleep(2)

# TODO Eventually we will have to create a dedicated setup
# where you can rename the assistant and set other preferences
# for now we'll have a placeholder name, Jim, and cross that
# bridge when we get to it

#TODO Remove the delay from the introduction to processing speech
def listener():
    speech = ""
    while True:
        #TODO clear this variable after a few minutes

        with mic as source:

                r.adjust_for_ambient_noise(source,duration = 1)
                print("Listening")
                audio = r.listen(source)

                try:
                    # TODO Switch this back to sphinx when done testing
                    speech = r.recognize_google(audio)
                    print(speech)
                # TODO Change Jim to the name variable
                    if "hey Jim" in speech or "Hey Jim" in speech:
                        engine.say("Yes?")
                        engine.runAndWait()
                        break
                except sr.UnknownValueError:
                    pass
                except sr.RequestError:
                    engine.say("I can not access the API")
                except:
                    # TODO Eventually remove this once everything is working
                    print("Something went wrong")
                print("done")

def speak():
    request = ""

    with mic as source:

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

    return(request)

engine.runAndWait()
listener()
action = speak()

print(action)

# SEARCHING THE INTERNET
# TODO Put custom questions in here like who are you?
if "what" in action or "who" in action or "when" in action or "where" in action or "why" in action or "how" in action:

    engine.say("Searching for," + action)
    engine.runAndWait()

    firefoxOptions = webdriver.FirefoxOptions()
    firefoxOptions.set_headless()

    opts = Options()
    opts.headless = True

    # Search engines generate results using JavaScript
    # so we can not use bs4 and requests in order to
    # scrape duckduckgo with just a http request.
    #
    # Instead we can generate the site with selenium and
    # try to scrape from there

    # Then if they are unavailable we will have to look at
    # summaries of different articles


    # TODO Optimize this especially the except clause since searches are slow
    try:
        driver = webdriver.Firefox(options=opts)
        driver.get("https://duckduckgo.com/?q=" + action)
        # Try to find the sidebar wikipedia module
        ans = driver.find_element_by_xpath("/html/body/div[2]/div[5]/div[3]/div/div[2]/div[2]/div/div/div[1]/div/div[2]/span")
    except:
        opts.headless = False
        driver = webdriver.Firefox(options=opts)
        driver.get("https://duckduckgo.com/?q=" + action)
        # Instead of reading the article we can instead do what similar
        # assistants do and just show the user the article since the
        # assistant will also have a GUI. Then say this is what i found

        engine.say("Ok this is what I found online on" + action)
        engine.runAndWait()

    try:
        print(ans.text)
        engine.say(ans.text)
        engine.runAndWait()
    except NameError:
        pass
    listen()


# PLAYING MUSIC/VIDEO
# TODO Come back to the development of play
if "play" in action or "Play" in action:
    player = mpv.MPV()

	#We're going to have to get some sort of media player
	#I'm leaning towards vlc

	#TODO check if play is empty or not
    driver = webdriver.Firefox(firefox_profile=profile)

    playPattern = re.compile(".*Play.",re.IGNORECASE)
    search = re.sub(playPattern,"",action)
    engine.say("Searching for " + search)
    search = re.sub("\s","+",search)
    engine.runAndWait()

    req = requests.get("https://www.youtube.com/results?search_query=" + search,headers=headers).text
    print("https://www.youtube.com/results?search_query=" + search)

    driver.get("https://www.youtube.com/results?search_query=" + search)

    #TODO Find a way to find the url of the first result of the Youtube search

    vid = driver.find_element_by_xpath("//*[@id=\"thumbnail\"]")

    url = vid.get_attribute("href")

    title = re.sub("[+]"," ",search)
    engine.say("Now Playing: " + title)
    engine.runAndWait()
    driver.close()
    
    @player.on_key_press("q")
    def q():
        print("stop")

    #TODO Run mpv headless
    player.play(url)
    player.wait_for_playback()
    player.wait_until_playing()
    print("playing")
    #TODO This does not get played since the .play is being ran


  
    #TODO Eventually work on pausing playing and rewinding

    # TODO Implement a way to stop the video when it is done

	#If we want we can separate requests between music and videos and have Spotify
	#handle music while we deal with videos on Youtube

