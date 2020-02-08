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

import country_converter as coco
from newsapi import NewsApiClient

from api.api_keys import weather_pyowm_api_key, getlocation_access_token_ipinfo, newsapi_api_key

from NLU.preprocess import stopWord_removal
from youtube_first_link import get_first_link
from NLU.pos_tagging import finding_nouns
from first_setup import *

from database.sqlite_queries import *

# https://github.com/gourabdg47/jarvis.git

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

init_db_name = "database\\db\\initial_db.db" #first_time_save_to_database.db_name #
init_table_name = "init_info_table"
todo_table_name = "todo_table"

global CREATOR
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



def getLocation(get_weather = False):

    access_token_ipinfo = getlocation_access_token_ipinfo

    handler = ipinfo.getHandler(access_token_ipinfo)
    details = handler.getDetails()
    
    if get_weather == True:
        getWeatherReport(details)
    else:
        return details.country_name  
    

def welcome(USERNAME):
    

    hour = int(dt.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good morning {}".format(USERNAME))
        # country_user_from = getLocation(get_weather = True) -----------------
        speak("How may I help you ?")

    elif hour>=12 and hour < 18:
        speak("Good afternoon {}".format(USERNAME))
        speak("How may I help you ?")

    elif hour>=18 and hour < 24:
        speak("Good evening {}".format(USERNAME))
        speak("How may I help you ?")

    else:
        speak("Good night {}".format(USERNAME))
        speak("How may I help you ?")
     

def takeCommand():
    r = sr.Recognizer()
    # put try except here -----------------
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Listening ...")
        audio = r.listen(source,  timeout = 3)


        try:
            print("Recognizing ...")
            query = r.recognize_google(audio, language = 'en-in')
            print('r.energy_threshold: ', r.energy_threshold)

            print("User said: {}\n".format(query))

        except Exception as e:
            print("Exception created: ", e)
            speak(
                "I couldn't understand what you said! Would you like to repeat?")
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

def news_fetch(type_, topic, country = 'us'):

    country = standard_names = coco.convert(names = country, to='ISO2')

    # Init
    newsapi = NewsApiClient(api_key = newsapi_api_key)

    try:
        while('' in topic):
            topic.remove("")

        for i, val in enumerate(topic):
            print("news_fetch, topic[i]: ",topic[i] )
            topic = topic[i]   

    except :
        pass              

    print('in news_fetch, topic: {}, type: {}, country: {}'.format(topic, type_, country))

    if type_ == 'headline' or type_ == 'headlines':
        
        # /v2/top-headlines
        top_headlines = newsapi.get_everything(q= topic,
                                                sources='bbc-news,the-verge',
                                                domains='bbc.co.uk,techcrunch.com',
                                                language='en',
                                                page_size = 5)

        articles = top_headlines['articles']

        if top_headlines['totalResults'] == 0:
            speak('Sorry, no news headlines found')
        else:

            speak("Todays top 5 news headlines on {} are ".format(topic)) 

            for i, val in enumerate(articles):
                print((i), val['title'])
                speak(val['title'])
        
        #speak("Todays top 5 news headlines on {} are {}".format(topic, top_headlines)) 

    elif type_ == "just_news:":
        # /v2/everything
        all_articles = newsapi.get_everything(q=topic,
                                            sources='bbc-news,the-verge',
                                            domains='bbc.co.uk,techcrunch.com',
                                            from_param='2017-12-01',
                                            to='2017-12-12',
                                            language='en',
                                            sort_by='relevancy',
                                            page=2)

        print("Full news:\n", all_articles)
        speak(all_articles)                                        
    
    # /v2/sources
    sources = newsapi.get_sources()


def tasks(query, search_query, country_user_from, search_query_nouns=None):
    
    news_headline_keywords = ['news', 'headline']
    news_keywords = ['test']

    print("in tasks(), search_query_nouns: ", search_query_nouns)

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

        try:
            new_query = query.replace('in YouTube', '')
        except:
            pass
        try:
            new_query = new_query.replace('from YouTube', '')
        except:
            pass
        try:
            new_query = new_query.replace('play', '')
        except:
            pass    
        new_query = new_query.replace(' ', '+')
        link = "https://www.youtube.com/results?search_query="+new_query
        print("Opening link: ", link)
        first_link = get_first_link(link)

        webbrowser.open(
            "https://www.youtube.com{}".format(first_link))
    
    elif "weather" in search_query.lower():
        getLocation(get_weather = True)

    elif "time" in search_query.lower():
        now = dt.now().time()
        
        speak("the time is, "+now.strftime('%I:%M:%S'))

    elif "date" in search_query.lower():
        date = dt.now().date()
        speak("today's date is, "+str(date))

    elif any(c in search_query_nouns for c in news_keywords):
        for n, val in enumerate(search_query_nouns):
            if val == 'news':
                search_query_nouns[n] = ""

        search_query = search_query.lower().replace('news', ' ')
        search_query = search_query.lower().replace('headline', ' ')
        
        print("calling news")
        news_fetch(type_ = 'just_news', topic = search_query_nouns, country = country_user_from)

    elif all(c in search_query_nouns for c in news_headline_keywords):

        for n, val in enumerate(search_query_nouns):
            if val == 'news' or val == 'headline':
                search_query_nouns[n] = ""

        
        search_query = search_query.lower().replace('news', '')
        search_query = search_query.lower().replace('headline', '')
        print("In task(), headline, search_query: ", search_query)

        print("calling news headlines")
        news_fetch(type_ = 'headline', topic = search_query.lower(), country = country_user_from)

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
            select_status, INIT_STATUS, USERNAME = select_query(init_table_name, init_db_name)

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

    try:
        country_user_from = getLocation(get_weather = False)
    except :
        pass    
    welcome(USERNAME)

    while 1:

        query = takeCommand()
        ## put try exception here -----------------------
        search_query = stopWord_removal(query)
        print("in main() after stop word removal: ",search_query)

        if re.search(r'\b(exit|quit|goodbye|goodbyejarvis|goodnight)\b', search_query, re.I):
            if search_query == "goodnight":
                speak('goodight sir')
                break
            else:
                speak('Bye sir')
                break
        
        search_query_nouns = finding_nouns(search_query)
        print("in main() after search_query_nouns: ",search_query_nouns)

        tasks(query, search_query, country_user_from, search_query_nouns)
    

#main starts here ---

if __name__ == "__main__": 
    main()