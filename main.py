import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import re
import smtplib
import ipinfo
import pyowm
from datetime import datetime as dt
import platform
import socket
from bs4 import BeautifulSoup
import requests

from api.api_keys import weather_pyowm_api_key, getlocation_access_token_ipinfo
from NLU.preprocess import stopWord_removal
from NLU.pos_tagging import finding_nouns
from youtube_first_link import get_first_link
from first_setup import *

from database.sqlite_queries import *

# https://github.com/gourabdg47/jarvis.git

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

init_db_name = "database\\db\\initial_db.db" #first_time_save_to_database.db_name #
init_table_name = "init_info_table"
todo_table_name = "todo_table"

CREATOR = "Gourab"

def system_details():
    platform = platform.system()
    os = os.name()

    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def getWeatherReport(location):

    pyowm_api_key = weather_pyowm_api_key

    owm = pyowm.OWM(pyowm_api_key) 
    observation = owm.weather_at_place(location.city)
    w = observation.get_weather()
    city = location.city
    wind_speed = w.get_wind()
    humidity = w.get_humidity() 
    c_temperature = w.get_temperature('celsius')

    speak("Today's weather details are Current City is {}, Humidity is {}, present temperature is {} celsius, today's maximum temperature is {} celsius and minimum temperature is {} celsius".format(city, humidity, round(c_temperature['temp']), round(c_temperature['temp_max']), round(c_temperature['temp_min'])))
    print("City: {}\nWind speed: {}\nHumidity: {}\nTemperature(Celsius): {}".format(city, wind_speed, humidity, c_temperature))


def getLocation():

    access_token_ipinfo = getlocation_access_token_ipinfo

    handler = ipinfo.getHandler(access_token_ipinfo)
    details = handler.getDetails()

    getWeatherReport(details)
    

def welcome():

    hour = int(dt.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good morning {}".format(CREATOR))
        getLocation()
        speak("How may I help you ?")

    elif hour>=12 and hour < 18:
        speak("Good afternoon {}".format(CREATOR))
        speak("How may I help you ?")

    elif hour>=18 and hour < 24:
        speak("Good evening {}".format(CREATOR))
        speak("How may I help you ?")

    else:
        speak("Good night {}".format(CREATOR))
        speak("How may I help you ?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening ...")
        audio = r.listen(source)

        try:
            print("Recognizing ...")
            query = r.recognize_google(audio, language = 'en-in')
            print('r.energy_threshold: ', r.energy_threshold)

            print("User said: {}\n".format(query))

        except Exception as e:
            print("Exception created: ", e)
            query = None

            return(takeCommand())

        except sr.UnknownValueError:
            speak(
                "I couldn't understand what you said! Would you like to repeat?")
            return(takeCommand())
        except sr.RequestError as e:
            print("Could not request results from " +
                "Google Speech Recognition service; {0}".format(e))

    return query

def search_wikipedia(query):

    results = wikipedia.summary(query, sentences=2)
    speak(results)


def tasks(query, search_query, search_query_nouns=None):

    if "wikipedia" in search_query.lower():
    
        noun_sentence = ' '.join(word for word in search_query_nouns)
        new_query = query.replace('wikipedia', '')
        print("NEW SENTENCES: ", new_query)

        try:
            search_wikipedia(new_query)
        except Exception as e:
            print('please give proper query, \nexception {}'.format(e))
            speak(e)
    
    elif "youtube" in search_query.lower():

        new_query = query.replace('in YouTube', '')
        new_query = new_query.replace(' ', '+')
        link = "https://www.youtube.com/results?search_query="+new_query
        print("Opening link: ", link)
        first_link = get_first_link(link)

        webbrowser.open(
            "https://www.youtube.com{}".format(first_link))
    
    elif "weather" in search_query.lower():
        getLocation()

    elif "time" in search_query.lower():
        now = dt.now().time()
        
        speak("the time is, "+now.strftime('%I:%M:%S'))

    elif "date" in search_query.lower():
        date = dt.now().date()
        speak("today's date is, "+str(date))

    else:
        pass


def create_todo():
    pass

    
def playMusic():
    # music using  pyspotify, spotify

    pass


def main():
    
    ## FIrst setup (One time) ##############
    # Checking initial status from database-
    # * check if the database is there or not 1st then status u dummy :)

    while 1:
        try:
            select_status, INIT_STATUS = select_query(init_table_name, init_db_name)

            if INIT_STATUS == 'True':
                break
            else:
                pass
        except:
            while 1:
                INIT_STATUS = init_setup()

                if INIT_STATUS == False:
                    INIT_STATUS = init_setup()
                else:
                    break                   
  
    #############

    welcome()
    while 1:

        query = takeCommand()
        
        search_query = stopWord_removal(query)

        if re.search(r'\b(exit|quit|goodbye|goodbyejarvis|goodnight)\b', search_query, re.I):
            if search_query == "goodnight":
                speak('goodight sir')
                break
            else:
                speak('Bye sir')
                break
        
        search_query_nouns = finding_nouns(search_query)

        tasks(query, search_query, search_query_nouns)
    

#main starts here ---

if __name__ == "__main__": 
    main()