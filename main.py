import speech_recognition as sr
from gtts import gTTS
import pyautogui
import datetime
import requests
import json
from pathlib import Path
import re
import smtplib
from apiclient.discovery import build
import webbrowser
from playsound import playsound
import os
from googletrans import Translator
from os import path
import wikipedia
from bs4 import BeautifulSoup
import time
from tkinter import *
import tkinter as tk
from tkinter import messagebox
import ctypes
import threading
try:
    from plyer import notification
except Exception as e:
    print(e)
try:
    import pywhatkit
except Exception as e:
    print(e)
# importing webdriver from selenium
from selenium import webdriver

def error_message(title, body, choice):
    dest = 'kn'
    # using switch like statement
    error_dict = {
        1: tk.messagebox.showinfo,
        2: tk.messagebox.showwarning,
        3: tk.messagebox.showerror
    }
    error_func = error_dict.get(choice, " ")
    # text_translator(title, lang["display-text"]), text_translator(body, lang["display-text"])
    error_func(title,body)
# icon settings required for app
icon = {
    "error": "images/err.ico",
    "message": "images/msg.ico",
    "tkinter-title-icon": "images/assistant.png",
}
# email settings
# or allow your email to allow less access app
# https://myaccount.google.com/u/1/lesssecureapps?pli=1&rapt=AEjHL4O0UCaKtEfNkfJKvAzInk7G9mo4V2lg4XrIEx-nANI2RESnzbL0i89O00Z3XpaHwn4qGezXUBSj0rH8ata2Y7BUSpKb-A
# or enable 2 step verification get user password here:
# https://accounts.google.com/signin/v2/challenge/pwd?continue=https%3A%2F%2Fmyaccount.google.com%2Fapppasswords%3Frapt%3DAEjHL4PPLXFxTp2CZQRcKbfyFBxtB1PhjJoQbqEKyTPiGr8KzRiY2J5xWyrMVtqZMUj5UJy2xhYAMsa3gt6u4TavdZUwHrgcpg&service=accountsettings&osid=1&rart=ANgoxcfU2c6rFQV2BWmEYkNTsYfGyg7qk7-prt9OPtubtg_Td7loS2wQJkdtAw2sfNIV2e9DD6euAnoqg9CDFOiTXLmIg00B0A&TL=AM3QAYYyne4Ju381Wae5dghRM7rniIAdVvGYhwZfQHRfyfrs80RPeKNsUNoLOp6l&flowName=GlifWebSignIn&cid=1&flowEntry=ServiceLogin
sender_email_info = {
    'user_name': '',
    'user_password': os.getenv('device_mail_id')
}
# Language settings default en,kn,kn
lang = {
    'display-text': 'en',
    'input-speech': 'kn',
    'output-speech': 'kn',
}
# Api key settings
# weather api key link
# https://openweathermap.org/api -> choose current weather data
# news api key link
# https://newsapi.org/ -> get api key
# create youtube api go to google
# https://console.cloud.google.com/apis/dashboard
# learn about api here https://developers.google.com/youtube/v3

api_keys = {
    'news_api': os.getenv('newsapi_api_key'),
    'weather_api' : os.getenv('weather_api_key'),
    'youtube_api': os.getenv('youtube_api_key')
}
# Error code settings
error_codes  = {
    'internet-error': {
        'etks':1000,
        'newsteller':1001,
        'weather-report':1003,
        'browser-open':1004,
        'google-search':1005,
        'youtube-link':1006,
        'mail':1007
    },
    'unknown-error': {
        'newsteller':1008,
        'notification':1009,
        'weather-report':1010,
        'google-maps':1011,
    },
    'dir-error':{
        'dir':1012,
    },
    'whatsapp':{
        'msg-error':1013,
    },
    'power':{
        'tweak-power':1014,
    }

}
# Array of bad words
bad_words = ['ಮುಕುಳಿ', 'ಕೆಯ', 'ನಾಯಿ ಕತ್ತೆ', 'ತುಲ್ಲೇ', 'ತುಲ್ಲಗ್', 'ತುಲ್ಲ', 'ತುನ್ನಿ', 'ಬೋಸುಡಿ', 'ಬೆವರ್ಸಿ', 'ಹಡ್ಬೆ',
             'ಸೂಳೇ',
             'ಸಾಟ', 'ಶಾಟ', 'ಹಲ್ಕಟ್', 'ಅಲ್ಕಟ್', 'ಹಲ್ಕಾಟ್', 'ಮಿಂಡ್ರೀ', 'ಮಿಂಡಾ', 'ಬಡ್ಡಿ', 'ಮುಂಡೆ', 'ಫಕ್', 'ಲೋಫರ್',
             'ನಿಮ್ಮಜ್ಜಿ', 'ಕತ್ತೆ', 'ಮಂಗ', 'ಸುವರ್', 'ಗಂಜರ್', 'ಬಿಚ್', 'ಪೀಸ್', 'ಬ್ಲಡಿ', 'ಹೆಲ್', 'ನಾಯಿ', 'ವಡ್ಡ']


# Tests if any of the array of words is present in given line
def testifarrayinline(arr, line):
    # It takes array of string and string line,
    # for every string in array put the string to elem
    for elem in arr:
        # if elem in line:
        if re.search(elem, line):
            return True
    return False


def return_searched_word(arr, line):
    # It takes array of string and string line,
    # for every string in array put the string to elem
    for elem in arr:
        # if elem is in line:
        if re.search(elem, line):
            return elem
    return False


def send_mail():
    try:
        from_mail=sender_email_info['user_name']
        frommail_password=sender_email_info['user_password']
        display('Speak the message you want to send when i am listening', 4)
        etks('Speak the message you want to send when i am listening')
        ggap()
        content = recursive_input('kn')
        content = text_translator(content, 'en')
        display('Enter the target email to which you want to send email and then press submit', 4)
        global inputValue
        block.set(True)
        root.wait_variable(block)
        to_mail = inputValue
        etks('email is being sent please wait')
        notify_system("ಸಂದೇಶ ಕಳುಹಿಸುವ ಪ್ರಕ್ರಿಯೆ ಪ್ರಾರಂಭವಾಗಿದೆ",to_mail+ 'ಗೆ ಕಳುಹಿಸಲಾಗುವುದು', icon['message'], 10)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(from_mail, frommail_password)
        server.sendmail(from_mail,to_mail, content)
        server.close()
    except Exception as e:
        error_message(f"Error e[{error_codes['internet-error']['mail']}]",'Cannot send mail ',3)
        print("Error inside [sendmail]")
    else:
        display('Successfully sent message', 4)
        etks("Email has been sent successfully")
    # mxsxmvkvdkvirtul


# This function accepts a command from the user in speech form
def takeuserinput(lang='kn', msg='Listening...'):
    # It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(msg)
        display(msg, 2)
        # hear=True
        r.pause_threshold = 0.6
        audio = r.listen(source)

    try:
        # hear = False
        display("Recognizing......", 2)
        print("Recognizing...")
        query = r.recognize_google(audio, language=f'{lang}-in')
        clear_display(heading_text1)
        display("Processing...", 2)
        display(query, 3)
        # print(f"User said: {query}\n")

    except Exception as e:
        print(e)
        clear_display(heading_text2)
        print("Please only speak when I am listening", e)
        display("Please only speak when I am listening", 2)
        ggap(4)
        # etks("Please say that again when i am listening")
        return None
    return query


# Open website function
def open_website(website, new_tab=0):
    try:
        # Try to open website url
        webbrowser.open_new(website)
    except Exception as e:
        error_message(f"Error e[{error_codes['internet-error']['browser-open']}]", 'An error occurred while opening browser', 3)
        print("Error while opening website [open_website]"+e)


# Playing music function
def say(music):
    # Use playsound and not play using os module because playsound plays syncronously while
    # play using os module plays asyc leading to misbehaving of current app
    playsound(music);


# English to Kannada or vice versa text function
def text_translator(text, dest='kn'):
    try:
        # keep this for emergency incase if other code does not works
        # from google_trans_new import google_translator
        # translator = google_translator()
        # translate_text = translator.translate(text, lang_tgt=dest)
        # 'Hola mundo!', lang_src = 'en'
        # print(translate_text)
        translator = Translator()
        translation= translator.translate(text, dest=dest)
        translate_text = translation.text
    except Exception as e:
        print('Error while text translation [text_translator]',e)
        translate_text = "Sorry error occurred"
    return translate_text


# English text to kannada speech function
def etks(text, id=1):
    dir = f"music//eng{id}.mp3"
    try:
        kan_txt = text_translator(text, 'kn')
        # gui.heading_display(kan_txt)
        display(kan_txt, 4)
        print(kan_txt)
        obj = gTTS(text=kan_txt, slow=False, lang='kn')
        obj.save(dir)
        say(dir)
        os.remove(dir)
    except Exception as e:
        error_message(f"Error e[{error_codes['internet-error']['etks']}]",'No Internet for text translation',3)
        print("No Internet for text translation and speech in [etks] :", e)


# News speaking function
def newsteller(number=10, country='in', category='&category=business', q='&q=tesla'):
    x = []
    api_key = api_keys['news_api']
    url = f'https://newsapi.org/v2/top-headlines?country={country}&language=en&apiKey={api_key}'
    try:
        x = requests.get(url, timeout=5)
        # parse and get json from response
        x = json.loads(x.text)
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("Internet problem occurred inside [newsteller]")
        error_message(f"Error e[{error_codes['internet-error']['newsteller']}]", 'No Internet for fetching News', 3)
    counter = 0
    try:
        # if length is not empty, meaning response has arrived then only enter
        if len(x) != 0:
            # enumerate gives position and object
            for id, cray in enumerate(x['articles']):
                counter += 1
                # counter is used to track number of news told
                if counter > int(number):
                    # if number of news has reached user told limit then break out of the loop
                    break
                regexp = '.*\s-\s'
                # patters to eliminate unrequired info
                pattern = re.compile(r'.*\s-\s')
                result = re.search(pattern, cray['title'])
                etks(f"News number {id + 1}")
                # speak re searched string
                etks(result.group(), id)
    except Exception as e:
        print("Error occurred inside [newsteller] :", e)
        error_message(f"Error e[{error_codes['unknown-error']['newsteller']}]",e, 3)


# Wish according to time function
def wish_time(time=datetime.datetime.now().strftime("%H")):
    # convert string time to int type
    time = int(time)
    # these are self explanatory
    if 5 < time < 12:
        etks(f"Good morning")
    elif 12 <= time < 17:
        etks(f"Good Midday")
    elif 17 <= time < 19:
        etks(f"Good Evening")
    else:
        etks(f"Good Night")


# Bad word checker function
def bwc(cmd):
    for bw in bad_words:
        # if bw in cmd:
        if bw in cmd:
            # ಇದುನ್ನಾ ನಿನ್ನ ಅಪ್ಪಂಗೆ ಹೇಳು
            etks(f"{bw} ನಿನ್ನಪ್ಪ", 5)
            break
    return


# Current time enquiry function
def curtime():
    etks(datetime.datetime.now().strftime("%H : %M "))


# Give gap function
def ggap(tim=0.5):
    time.sleep(tim)


# fuction to create a directory,this function creates all dirs in dir_array
def create_dir(dir_array):
    # pick particular directory from directory array
    for dir in dir_array:
        # If directory path does not exists then only proceed,because there is no point in creating same dir
        if not (path.exists(dir)):
            try:
                # try to make directory
                os.mkdir(dir)
            except Exception as e:
                print("Not able to make music directory inside [create_dir] :", e)
                error_message(f"Error e[{error_codes['dir-error']['dir']}]", 'Not able to make directory', 3)


# funtion to clear all files inside a directory,this function clears entire dir inside dir_array
def clear_dir(dir_array):
    # pick particular directory from directory array
    for dir in dir_array:
        # If directory path exists then only proceed
        if path.exists(dir):
            try:
                # create list of files in a particular dir using list comprehension
                filelist = [f for f in os.listdir(dir)]
                for f in filelist:
                    # for all files inside filelist array remove the file
                    # join dir path with file path to find file location and delete that
                    os.remove(os.path.join(dir, f))
            except Exception as e:
                print("Not able to make music directory inside [clear_dir] :", e)
                error_message(f"Error e[{error_codes['dir-error']['dir']}]", 'Not able to make directory', 3)


# Initialization function
def init():
    wish_time()
    ggap()
    etks("I am kashvi,please tell me how may i help", 1)


# Send whats app message function
def swm():
    try:
        etks("Speak the message you want to send when I start to listen")
        # Calculate current time hour,min,sec
        ggap()
        msg = takeuserinput('kn', 'Listening to message')
        # Take number to which user wants to send message
        display('Enter the target email to which you want to send email and then press submit', 4)
        global inputValue
        block.set(True)
        root.wait_variable(block)
        num = inputValue
        hr = int(datetime.datetime.now().strftime("%H"))
        mn = int(datetime.datetime.now().strftime("%M")) + 1
        sec = int(datetime.datetime.now().strftime("%S"))
        if sec > 30:
            mn = mn + 1
        notify_system("ವಾಟ್ಸಪ್ ಸಂದೇಶ ಕಳುಹಿಸುವ ಪ್ರಕ್ರಿಯೆ ಪ್ರಾರಂಭವಾಗಿದೆ",
                      '"' + msg + ' "ಎಂಬ ಸಂದೇಶವನ್ನು ' + num + 'ಗೆ ಕಳುಹಿಸಲಾಗುವುದು', icon['message'], 10)
        # send message using pywhatkit module
        pywhatkit.sendwhatmsg('+91' + num, msg, hr, mn)
    except:
        print("Message can't be sent in [swm]",e)
        error_message(f"Error e[{error_codes['whatsapp']['msg-error']}]", 'An error while sending message', 3)
    else:
        etks("Whatsapp message has been sent successfully")


# Notification function to show notification to system
def notify_system(title, message, app_icon, timeout=4):
    try:
        notification.notify(
            title=title,
            message=message,
            app_icon=app_icon,
            timeout=timeout,
            toast=False
        )
    except Exception as e:
        print("Error occurred inside [notify_system]")
        error_message(f"Error e[{error_codes['unknown-error']['notification']}]",e,3)


def utc_to_time(secsTillEpoch):
    # ctime converts epoch to string ex:1618965725 -> Wed Apr 21 06:12:05 2021
    local_time = time.ctime(secsTillEpoch)
    # strptime function parses from string
    cur_time = datetime.datetime.strptime(local_time, '%a %b %y %H:%M:%S %Y')
    return cur_time


# Enter latitude and longitude to get weather information
def weather_report(latitude=13.66675, longitude=75.30914):
    api_key = api_keys['weather_api']
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid" \
          f"={api_key}&lang=en "
    json_object = {}
    w = {}
    try:
        etks("Information about weather is being fetched ,please wait")
        json_object = json.loads(requests.get(url).text)
        w = json_object
        # print(type(json_object))
    except Exception as e:
        print("Internet problem ocurred in [weather_report]", e)
        error_message(f"Error e[{error_codes['internet-error']['weather_report']}]", 'Internet problem occured while weather fetching', 3)
    json_formatted_str = json.dumps(json_object, indent=2)
    # Check if dictionary is empty
    if len(w) != 0:
        try:
            # SunriseSeconds are in form ex:1618965725
            sunRiseSeconds = json_object['sys']['sunrise']
            sunSetSeconds = json_object['sys']['sunset']
            # json_object['main']['sunrise']
            # Sunrise/Sunset time is an object contining properties like hour,minute,etc
            sunRiseTime = utc_to_time(sunRiseSeconds)
            sunSetTime = utc_to_time(sunSetSeconds)
            # Information about wind like speed,direction in degree
            windInfo = f"  Wind is blowing at the speed of {w['wind']['speed']} and at direction of {w['wind']['deg']} degree."
            # Information about weather type and condition and also cloud percentage
            weatherInfo = f"  Today's weather  is {w['weather'][0]['main']} and has weather condition {w['weather'][0]['description']}.Cloud percentage is {w['clouds']['all']}."
            # Information about temperature in celsius.Temperature is first converted to degree form kelvin and is fed to round fuction which rounds up to two digit
            temperatureInfo = f"  Temperature is {round(w['main']['temp'] - 273.1, 2)} degree Celsius and it is feeling like {round(w['main']['feels_like'] - 273.15, 2)} degree Celsius."
            # Information about pressure in pascal
            pressureInfo = f"  Pressure is {w['main']['pressure'] * 100} Pascal."
            # Information about humidity in percentage
            humidityInfo = f"  Humidity is {w['main']['humidity']}%."
            # Information of sunrise
            sunRiseInfo = f"Expected sunrise {str(sunRiseTime.hour) + ':' + str(sunRiseTime.minute)} and "
            # Information of sunset
            sunSetInfo = f"Expected sunset {str(sunSetTime.hour) + ':' + str(sunSetTime.minute)}"
            # Speak all info through etks function
            etks(windInfo + weatherInfo + temperatureInfo + pressureInfo + humidityInfo + sunRiseInfo + sunSetInfo)
        except Exception as e:
            print("Error occurred [inside weather_report]:", e)
            error_message(f"Error e[{error_codes['unknown-error']['weather-report']}]", e, 3)
    else:
        notify_system("Error",
                      'Sorry !!!: Cannot access weather information.There was a problem connecting with server check your internet and then retry.',
                      icon["error"], 8)


def wikipedia_search(query, sentences=2):
    try:
        query = text_translator(query, dest='en')
        # etks(f"Searching wikipedia about {query}")
        # print(query)
        result = wikipedia.summary(query, sentences=sentences)
        print("result:", result)
        etks("According to wikipedia")
        etks(result)
    except Exception as e:
        print('Error occurred inside [wikipedia_search]:',e)
        # "ಕ್ಷಮಿಸಿ ಯಾವುದೇ ಮಾಹಿತಿ ಇಲ್ಲ"
        etks("Sorry there is no information")


commands = {
    'time': ['ಟೈಮ್', 'ಟೈಮ್ ಎಷ್ಟು', 'ಗಂಟೆ ಎಷ್ಟು', 'ಟೈಮೆಷ್ಟು', 'ಸಮಯ ಎಷ್ಟು', 'ಸಮಯವೆಷ್ಟು'],
    'news': ['ವಾರ್ತೆ ತಿಳಿಸು', 'ನ್ಯೂಸ್ ತಿಳಿಸು', 'ಮುಖ್ಯ ವಾರ್ತೆ ತಿಳಿಸು', 'ಸುದ್ದಿ ತಿಳಿಸು'],
    'wikipedia': ['ವಿಕಿಪೇಡಿಯ', 'ವಿಕಿಪಿಡಿಯಾ', 'ವಿಕಿಪೀಡಿಯ'],
    'you-tube': ['ಯೂಟ್ಯೂಬ್ ಅನ್ನು ತೆರೆಯಿರಿ', 'ಯೂಟ್ಯೂಬ್ ತೆರೆ', 'ಯುಟ್ಯೂಬ ಓಪನ್', 'ಓಪನ್ ಯುಟ್ಯೂಬ', 'ಓಪನ್ ಯುಟ್ಯೂಬ್',
                 'ಯುಟ್ಯೂಬ್ ','ಯೂಟ್ಯೂಬ್'],
    'google': ['ಗೂಗಲ್ ಅನ್ನು ತೆರೆಯಿರಿ', 'ಗೂಗಲ್ ತೆರೆ', 'ಗೂಗಲ್ ಓಪನ್', 'ಓಪನ್ ಗೂಗಲ್'],
    'weather': ['ವೆದರ್', 'ಹವಾಮಾನ', 'ವಾತಾವರಣ'],
    'whatsapp': ['ವಾಟ್ಸಪ್', 'ವಾಟ್ಸಾಪ್'],
    'restart': ['ರೀಸ್ಟಾರ್ಟ್ ಕಂಪ್ಯೂಟರ್','ಕಂಪ್ಯೂಟರ್ ರೀಸ್ಟಾರ್ಟ್', 'ಗಣಕಯಂತ್ರವನ್ನು ಮರು ಪ್ರಾರಂಭಿಸು',
                'ಗಣಕಯಂತ್ರವನ್ನು ಮರುಪ್ರಾರಂಭಿಸಿ'],
    'sleep': ['ಗಣಕಯಂತ್ರವನ್ನು ಮಲಗಿಸು', 'ಗಣಕಯಂತ್ರ ಮಲಗು','ಕಂಪ್ಯೂಟರ್ ಮಲಗು','ಕಂಪ್ಯೂಟರ್ ಮಲಗಿಸು',
                'ಸ್ಲೀಪ್ ಕಂಪ್ಯೂಟರ್', 'ಕಂಪ್ಯೂಟರ್ ಸ್ಲೀಪ್', 'ಮುಚ್ಕೋ ಮಲ್ಕ','ಮುಚ್ಕೊಂಡ್ ಮಲ್ಕೋ', 'ಮುಚ್ಕೊಂಡು ಮಲ್ಕ'],
    'power-off': ['ಕಂಪ್ಯೂಟರ್ ಕೆಡಿಸು', 'ಕಂಪ್ಯೂಟರ್ ಆರಿಸು', 'ಗಣಕಯಂತ್ರವನ್ನು ಆರಿಸು', 'ಗಣಕಯಂತ್ರವನ್ನು ಕೆಡಿಸು',
                  'ಶಟ್ ಡೌನ್ ಕಂಪ್ಯೂಟರ್', 'ಕಂಪ್ಯೂಟರ್ ಶಬ್ದೊನ್', 'ಕಂಪ್ಯೂಟರನ್ನು ಆರಿಸು'],
    'google-text': ['ಗೂಗಲ್', 'ಗೋಗಲ್', 'ಗಾಗಲ್'],
    'map': ['ಮ್ಯಾಪ್','ಮ್ಯಾಪ್ಸ್','ನಕ್ಷೆ'],
    'twitter':['ಟ್ವಿಟರ್ ತೆರೆ','ಟ್ವಿಟರ್ ಓಪನ್','ಓಪನ್ ಟ್ವಿಟರ್'],
    'facebook':['ಓಪನ್ ಫೇಸ್ಬುಕ್','ಫೇಸ್ಬುಕ್ ಓಪನ್','ಫೇಸ್ಬುಕ್ ತೆರೆ','ತೆರೆ ಫೇಸ್ಬುಕ್'],
    'instagram':['ಇನ್ಸ್ಟಾಗ್ರಾಮ್ ಓಪನ್','ಓಪನ್ ಇನ್ಸ್ಟಾಗ್ರಾಮ್','ತೆರೆ ಇನ್ಸ್ಟಾಗ್ರಾಮ್','ಇನ್ಸ್ಟಾಗ್ರಾಮ್ ತೆರೆ','ಓಪನ್ ಇನ್ಸ್ಟಾ'
        ,'ಇನ್ಸ್ಟಾ ಓಪನ್'],
    'e-mail':['ಇ-ಮೇಲ್ ಕಳಿಸು','ಇ-ಮೇಲ್','ಇಮೇಲ್ ಕಳುಹಿಸು'],
    'positive-statements': ['ಹೌದು', 'ಹಾ', 'ಎಸ್', 'ಓಕೆ'],
    'negative-statements': ['ನೋ', 'ಇಲ್ಲ', 'ಅಲ್ಲ'],
    'meaning':['ಶಬ್ದದ ಅರ್ಥ','ಶಬ್ದ ಅರ್ಥ','ಶಬ್ದಾರ್ಥ','ಮೀನಿಂಗ್'],
}


def tweak_power(command, action):
    try:
        etks(f"Are you sure want to {action} computer")
        # Ask for user confirmation
        if testifarrayinline(commands['positive-statements'], takeuserinput('kn')):
            etks(f"Now computer will {action}")
            os.system(command)
        else:
            etks(f"Computer will not {action} due to your action or inaction")
        # If error occurs then
    except Exception as e:
        etks(f"Some error has occurred inside [tweak_power]")
        error_message(f"Error e[{error_codes['power']['tweak-power']}]", 'Some error occured while tweaking power', 3)
        print(e)


def google_search(user_input="who is Prime Minister of India"):
    # if user wanted to search Meaning of the word
    try:
        if testifarrayinline(commands['meaning'], user_input):
            # replace words in commands['meaning'] array with ''
            query = user_input.replace(return_searched_word(commands['meaning'], user_input), '')
            # Translate kannada query to english
            english_query = text_translator(query,'en')
            # Append 'meaning of the word ' to get perfect search result
            apended_eng_query = 'meaning of the word '+ english_query
            # Request html data from this url
            result = requests.get(f"https://www.google.com/search?q={apended_eng_query}")
            html_text = result.text
            # Parse html data
            html_parsed = BeautifulSoup(html_text, 'html.parser')
            # Scrape html to find particular div which contains data using Beautiful soup
            # find_all finds all 'div' but [2] selects only third 'div'
            match = html_parsed.find_all("div", {"class": "BNeawe s3v9rd AP7Wnd"})[2]
            # speak result
            etks(match.text)
        else:
            # If user wants to know query a person
            # Translate kannada query to english
            user_input = text_translator(user_input, dest='en')
            # Request html data from this url
            result = requests.get(f"https://www.google.com/search?q={user_input}")
            html_text = result.text
            # Parse html data
            html_parsed = BeautifulSoup(html_text, 'html.parser')
            # Scrape html to find particular div which contains data using Beautiful soup
            # find method searches for first possible match of the div
            # Note here class is not used and class_ is used because class is a python keyword and hence can't use
            match = html_parsed.find('div', class_='BNeawe')
            # print(match.text.split(".", 1))
            etks(match.text)
    except EXCEPTION as e:
        error_message(f"Error e[{error_codes['internet-error']['google-search']}]", 'Internet problem occurred while google search', 3)
        print("An error occurred inside [google_search] :",e)


# Get youtube link ,note that you want api key for youtube.
def get_youtube_link(query):
    try:
        youtube = build('youtube', 'v3', developerKey=api_keys['youtube_api'])
        # search you tube for top results
        req = youtube.search().list(q=query, part='snippet', type='video')
        # grab top result video id.(video id is unique id given to every video by you tube)
        video_id = req.execute()['items'][0]['id']['videoId']
        # form you tube link from video id
        youtube_link = f'https://www.youtube.com/watch?v={video_id}'
        return youtube_link
    except Exception as e:
        error_message(f"Error e[{error_codes['internet-error']['youtube-link']}]", 'Fatal error occurred while getting you tube link', 3)
        print("Error occurred inside [get_youtube_link] :",e)


# Opens google maps using selenium tool
def open_google_maps(url):
    try:
        # set driver as global(It is necessary because if not set then browser closes itself after sometime)
        global driver
        # Here Chrome  will be used
        # Chrome driver location if not downloaded chromedriver download it from online
        driver = webdriver.Chrome('C:\Program Files (x86)\chromedriver.exe')
        # Opening the website
        driver.get(url)
        # Giving gap of 5 seconds
        ggap(5)
        # Geting the button by class
        button = driver.find_element_by_class_name("searchbox-searchbutton")
        # clicking on the search button on website
        button.click()
        # Giving gap of 2 seconds
        time.sleep(2)
        # click again search button
        button.click()
    except Exception as e:
        print("Error occurred inside [open_google_maps]",e)
        error_message(f"Error e[{error_codes['unknown-error']['google-maps']}]", 'No Internet for text translation', 3)


def recursive_input(lang='kn'):
    # Taking user input in kannada language
    # User user_input is in the format of  kannada string
    user_input = takeuserinput()
    # Take user input until he/she speaks something
    while user_input is None:
        user_input = takeuserinput()
    # return user input
    return user_input


count = 0
# Main function
def main():
    global count
    if count == 0:
        init()
        count+=1
    # Recursive input takes user from input until user speaks
    user_input = recursive_input('kn')
    # Only enter function if user input is not none
    if (user_input is not None) and (user_input != 'None'):
        # Checks for bad words
        bwc(user_input)
        # If user asks for time
        if testifarrayinline(commands['time'], user_input):
            curtime()
        # If user asks for news
        elif testifarrayinline(commands['news'], user_input):
            # etks("How many news do you want to hear")
            # takeuserinput('en', "Tell me how many news do you want to hear....")
            newsteller(2)
        # If user asks for wikipedia search
        elif testifarrayinline(commands['wikipedia'], user_input):
            wikiQuery = user_input.replace(return_searched_word(commands['wikipedia'], user_input), '')
            wikipedia_search(wikiQuery)
        # If user asks to open you tube browser
        elif testifarrayinline(commands['you-tube'], user_input):
            yt_query = user_input.replace(return_searched_word(commands['you-tube'], user_input), '')
            open_website(get_youtube_link(text_translator(yt_query,'kn')))
        # If user asks to open google in browser
        elif testifarrayinline(commands['google'], user_input):
            open_website("https://www.google.com")
        # If user asks to open google in browser
        elif testifarrayinline(commands['twitter'], user_input):
            open_website("https://twitter.com")
        # If user asks to open google in browser
        elif testifarrayinline(commands['facebook'], user_input):
            open_website("https://www.facebook.com")
        # If user asks to open google in browser
        elif testifarrayinline(commands['instagram'], user_input):
            open_website("https://www.instagram.com/")
        # If user asks for weather data
        elif testifarrayinline(commands['weather'], user_input):
            weather_report()
        # If user asks for message using whatsapp
        elif testifarrayinline(commands['whatsapp'], user_input):
            try:
                # call send whatsapp message
               swm()
            except Exception as e:
                print("Inside main in whatsapp",e)
        elif testifarrayinline(commands['e-mail'], user_input):
            send_mail()
        # If user asks for computer operation like on,off,restart
        elif testifarrayinline(commands['power-off'], user_input):
            # Power off fucntion
            tweak_power("shutdown /s /t 1", 'power-off')
        elif testifarrayinline(commands['restart'], user_input):
            # Restart fucntion
            tweak_power("shutdown /r /t 1", 'restart')
        elif testifarrayinline(commands['sleep'], user_input):
            # Sleep function
            tweak_power("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", 'sleep')
        # If user asks for Google search the given keyword
        elif testifarrayinline(commands['google-text'], user_input):
            # Google function
            # replace function replaces first parameter with second parameter
            # return searched word returns exactly key word used by user to trigger this elif block
            google_query = user_input.replace(return_searched_word(commands['google-text'], user_input), '')
            google_search(google_query)
        # If user asks for google map to show a village/city
        elif testifarrayinline(commands['map'], user_input):
            # Google map function
            map_query = user_input.replace(return_searched_word(commands['map'], user_input), '')
            # map_query = text_translator(map_query,'en')
            open_google_maps(f"https://www.google.com/maps/place/{map_query}")
        else:
            etks("Sorry I am not able to hear because of combined voice")
    # call main function recursively until stop button is pressed in gui
    main()


####################################################################################
# ----------------------------------- GUI DESIGN --------------------------------- #
####################################################################################

# Thread class
class thread_with_exception(threading.Thread):
    def __init__(self, func, name="Thread"):
        self.func = func
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        try:
            self.func()
        except Exception as e:
            print(e)

    def get_id(self):

        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                         ctypes.py_object(SystemExit))
        print(res, thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')


# When onstop method is pressed
def on_start():
    # Create all directories required for entire app to avoid error
    create_dir(['music','images','help','data'])
    display("Started", 1)
    clear_display(heading_text1, heading_text2, main_screen_text)
    # Grab global variables instead of function variables
    # If global is not specified function variables are called
    global t1, is_alive
    # t1 variable is none then
    if t1 is None:
        # Creating thread and assigning it to t1 global variable
        t1 = thread_with_exception(main, main)
        # Make it daemon thread so that it stops when tkinter gui exits
        # If daemon is not specified it does not quits even after exiting GUI
        t1.daemon = True
        # Thread is created but not started , lets do this
        t1.start()
        # Set variable so that to indicate thread is alive
        is_alive = True
    elif t1 is not None:
        # Only enter if thread is not alive
        if not is_alive:
            # Creating thread and assigning it to t1 global variable
            t1 = thread_with_exception(main, main)
            # Make it daemon thread so that it stops when tkinter gui exits
            # If daemon is not specified it does not quits even after exiting GUI
            t1.daemon = True
            # Thread is created but not started , lets do this
            t1.start()
            # Set variable so that to indicate thread is alive
            is_alive = True
        else:
            error_message("Warning", "App is already started", 2)


# When stop button is pressed
def on_stop():
    # Clear and update display
    clear_dir(['music'])
    clear_display(heading_text1, heading_text2, main_screen_text)
    display("App has Stopped,Press start", 1)
    display("Stopped", 2)
    display("Press start to start the program",4)
    # Grab global variables instead of function variables
    global t1, is_alive
    # t1 is thread 1 check if it is alive and only stop thread if thread is alive
    if is_alive:
        if t1 is not None:
            # Set is_alive = False indicating thread is dead
            is_alive = False
            # Stop thread by raising exception
            t1.raise_exception()
            # As thread is dead clear data inside t1 variable
            t1 = None
    else:
        error_message("Warning", "App is already stopped", 2)


# When restart button is pressed
def on_restart():
    on_stop()
    on_start()
    # Updated display
    display("Restarted", 1)


def clear_display(*args):
    # *args accepts set of commands as ex: clear_display(1,2) if we print(args) -> (1,2)
    for elem in args:
        # for all elements inside args apply set method
        # Set is a method of tkinter set("") which sets display to null/clears display
        elem.set("")


# On clear screen
def on_clear():
    clear_display(heading_text1, main_screen_text)


# Displays text on screen according to choice.There are four displays in the app
# Ex:display("Hello", 1) displays "Hello" on first display
def display(value, choice):
    # function switcher dictionary
    func_switcher = {
        1: notify_heading_text,
        2: heading_text1,
        3: heading_text2,
        4: main_screen_text,
    }
    # Get function according to user choice
    disp_func = func_switcher.get(choice, " ")
    # Append text to append
    text_switcher = {
        1: "App has ",
        2: "Condition  :",
        3: "Input   : ",
        4: "Output  : ",
    }
    # Get value according to choice of user if choice is invalid return " "
    # get is a dictionary method which returns value according to key if no key match returns second argument
    disp_text = text_switcher.get(choice, " ")
    disp_func.set(disp_text + value)


# Root timeout of tkinter (If using tkiner use this instead of time.sleep)
def timeout(sec, func):
    root.after(sec, func)


# Tweak volume of pc
def tweak_volume(volume_points, volume_up=True):
    # Check if user wants to raise volume else down volume
    if volume_up:
        # Raise volume_points*2 volume , ex: if volume_points is 10 it raises 20 paints
        for _ in range(volume_points):
            # Raises volume 2 points once called in windows
            pyautogui.press("volumeup")
    else:
        for _ in range(volume_points):
            # Downs volume 2 points once called in windows
            pyautogui.press("volumedown")


# If help function is called display and open default help.txt
def on_help():
    path = os.getcwd()
    # path.join is used to join path because even if we forget to put / it adds itself
    path_of_file = os.path.join(path, 'help/help.txt')
    os.startfile(path_of_file, 'open')


# themes and colors
theme = {
    'black_theme': {
        'app-bg': '#404040',
        'app-disp-bg': '#d1e7dd',
        'n1-txt': 'white',
        'h1-txt': '#0b3b24',
        'h2-txt': '#0b3b24',
        'main-txt': '#0f5132',
        'btn': {
            'start-bg': '#0275d8',
            'start-fg': 'white',
            'stop-bg': '#ff0000',
            'stop-fg': 'white',
            'rstart-bg': 'green',
            'rstart-fg': 'white',
        }
    },
    'white_theme': {
        'app-bg': 'white',
        'app-disp-bg': '#ffe7c9',
        'n1-txt': '#404040',
        'h1-txt': '#cc7100',
        'h2-txt': '#cc7100',
        'main-txt': '#e07c00',
        'btn': {
            'start-bg': '#0275d8',
            'start-fg': 'white',
            'stop-bg': '#ff0000',
            'stop-fg': 'white',
            'rstart-bg': 'green',
            'rstart-fg': 'white',
        }
    },
    'orange_theme': {
        'app-bg': '#ff7700',
        'app-disp-bg': '#ffd2ab',
        'n1-txt': 'white',
        'h1-txt': '#de5c00',
        'h2-txt': '#de5c00',
        'main-txt': '#ff6a00',
        'btn': {
            'start-bg': '#0275d8',
            'start-fg': 'white',
            'stop-bg': '#ff0000',
            'stop-fg': 'white',
            'rstart-bg': 'green',
            'rstart-fg': 'white',
        }
    },
    'blue_theme': {
        'app-bg': '#00ffee',
        'app-disp-bg': '#00a196',
        'n1-txt': '#404040',
        'h1-txt': '#960000',
        'h2-txt': '#960000',
        'main-txt': '#b50000',
        'btn': {
            'start-bg': '#0275d8',
            'start-fg': 'white',
            'stop-bg': '#ff0000',
            'stop-fg': 'white',
            'rstart-bg': 'green',
            'rstart-fg': 'white',
        }
    }
}


def change_theme(theme_name):
    # Changing theme of app
    notification1.configure(bg=theme_name['app-bg'], fg=theme_name['n1-txt'])
    heading1.configure(bg=theme_name['app-disp-bg'], fg=theme_name['h1-txt'])
    heading2.configure(bg=theme_name['app-disp-bg'], fg=theme_name['h2-txt'])
    main_screen.configure(bg=theme_name['app-disp-bg'], fg=theme_name['main-txt'])
    # Changing button theme color according to color
    start_btn.configure(bg=cur_theme['btn']['start-bg'], fg=cur_theme['btn']['start-fg'])
    stop_btn.configure(bg=cur_theme['btn']['stop-bg'], fg=cur_theme['btn']['stop-fg'])
    restart_btn.configure(bg=cur_theme['btn']['rstart-bg'], fg=cur_theme['btn']['rstart-fg'])
    root.configure(bg=theme_name['app-bg'])


def on_submit():
    global inputValue
    inputValue = textBox.get("1.0", "end-1c")
    print(inputValue)
    block.set(False)
    textBox.delete("1.0", 'end')
    print("done waiting.")


if __name__ == '__main__':
    # Set default theme of the app
    cur_theme = theme['black_theme']
    # global variables
    # t1 is thread one which is used to start or stop a thread
    t1 = None
    # is_alive is used to check is thread dead if it is alive then block start
    is_alive = False
    root = Tk()
    # set up block variable so that program can be blocked when required.(using tkinter block variable)
    block = BooleanVar(root, False)
    root.title(os.getcwd() + '\\' + Path(__file__).name)
    root.iconphoto(True, tk.PhotoImage(file=icon["tkinter-title-icon"]))
    # Gets the requested values of the height and widht.
    windowWidth = root.winfo_reqwidth()
    windowWidth = 400
    windowHeight = root.winfo_reqheight()
    windowHeight = 600
    print("Width", windowWidth, "Height", windowHeight)
    idth = root.winfo_reqwidth()
    # Gets both half the screen width/height and window width/height
    positionRight = int(root.winfo_screenwidth() / 2 - windowWidth / 2)
    positionDown = int(root.winfo_screenheight() / 2 - windowHeight / 2)
    # Positions the window in the center of the page.
    root.geometry("400x600+{}+{}".format(positionRight, positionDown))
    # root.resizable(0, 0)
    # Set minimum window size so that it can't be further reduced
    root.minsize(400, 600)
    # root.maxsize(401, 601)
    # Set text variables of variables so that they can be modified later to update display
    main_screen_text = tk.StringVar()
    heading_text1 = tk.StringVar()
    heading_text2 = tk.StringVar()
    notify_heading_text = tk.StringVar()
    out_txt = "Press Start to Start program"
    # Creating notification1 screen and styling it
    notification1 = Label(height=1, textvariable=notify_heading_text, bd=0)
    notification1.pack(fill=X, side=TOP)
    notification1.configure(bg=cur_theme['app-bg'], fg=cur_theme['n1-txt'], font=('Helvetica', 12, 'bold'), pady=10)
    # Creating heading1 screen and styling it
    heading1 = Label(height=1, wraplength=380, textvariable=heading_text1, bd=0)
    heading1.pack(fill=X, side=TOP)
    heading1.configure(bg=cur_theme['app-disp-bg'], fg=cur_theme['h1-txt'], font=('Helvetica', 16, 'bold'), pady=10)
    # Creating heading2 screen and styling it
    heading2 = Label(height=2, wraplength=380, textvariable=heading_text2, bd=0)
    heading2.pack(fill=X, side=TOP)
    heading2.configure(bg=cur_theme['app-disp-bg'], fg=cur_theme['h2-txt'], font=('Helvetica', 12, 'bold'), pady=10)
    # Creating main screen and styling it
    main_screen = Label(height=14, wraplength=380, textvariable=main_screen_text, bd=0)
    main_screen.pack(fill=BOTH, side=TOP, expand=TRUE)
    main_screen.configure(bg=cur_theme['app-disp-bg'], fg=cur_theme['main-txt'], font=('Helvetica', 12, 'bold'),
                          pady=10)
    # Set main screen text upon start of app
    main_screen_text.set(out_txt)
    textBox = Text(root, height=1, width=20)
    textBox.pack()
    submit_btn = Button(root, borderwidth=0, fg=cur_theme['btn']['start-fg'], activebackground='#025aa5',
           activeforeground='white',
           bg=cur_theme['btn']['start-bg'], text="Submit", command=lambda:on_submit(),
           font=('Helvetica', 8))
    # button = tk.Button(root, text="Click Me", command=lambda: var.set(1))
    # button.place(relx=.5, rely=.5, anchor="c")
    submit_btn.pack()


    # Show default display upon app start
    display("Stopped", 2)
    display("Stopped , Press Start", 1)
    # Start button creation and design and bg and fg are set to variable so that they can be controlled by change_theme function
    start_btn_txt = tk.StringVar()
    start_btn = Button(root, borderwidth=0, fg=cur_theme['btn']['start-fg'], activebackground='#025aa5',
                       activeforeground='white',
                       bg=cur_theme['btn']['start-bg'], textvariable=start_btn_txt, command=on_start,
                       font=('Helvetica', 12, 'bold'), padx=10, pady=6, )
    start_btn_txt.set('Start')
    start_btn.pack(side=LEFT)
    # Stop button creation and design and bg and fg are set to variable so that they can be controlled by change_theme function
    stop_btn_txt = tk.StringVar()
    stop_btn = Button(root, borderwidth=0, fg=cur_theme['btn']['stop-fg'], activebackground='#ed0202',
                      activeforeground='white', bg=cur_theme['btn']['stop-bg'],
                      textvariable=stop_btn_txt, command=on_stop, font=('Helvetica', 12, 'bold'), padx=10, pady=6)
    stop_btn_txt.set('Stop')
    stop_btn.pack(side=LEFT, padx=90, pady=10)
    # Restart button creation and design and bg and fg are set to variable so that they can be controlled by change_theme function
    restart_btn_txt = tk.StringVar()
    restart_btn = Button(root, borderwidth=0, fg=cur_theme['btn']['rstart-fg'], activebackground='#40556a',
                         activeforeground='white', bg=cur_theme['btn']['rstart-bg'],
                         textvariable=restart_btn_txt, command=on_restart, font=('Helvetica', 12, 'bold'), padx=10,
                         pady=6)
    restart_btn_txt.set('Restart')
    restart_btn.pack(side=RIGHT)
    # Create menubar
    menubar = Menu(root, relief=FLAT, bd=0)
    # First item on menubar and creates sub options
    appmenu = Menu(menubar, tearoff=0)
    # Add sub-menu options to appmenu
    appmenu.add_command(label="Start", command=on_start)
    appmenu.add_command(label="Stop", command=on_stop)
    appmenu.add_command(label="Restart", command=on_restart)
    appmenu.add_command(label="Clear", command=on_clear)
    appmenu.add_separator()
    appmenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="App", menu=appmenu)
    # Adds to menubar and creates sub options
    volumemenu = Menu(menubar, tearoff=0)
    volumemenu.add_command(label="Volume Up", command=lambda: tweak_volume(10, True))
    volumemenu.add_command(label="Volume Down", command=lambda: tweak_volume(8, False))
    volumemenu.add_command(label="Mute/unmute", command=lambda: pyautogui.press("volumemute"))
    menubar.add_cascade(label="Volume", menu=volumemenu)
    # Help menu to instruct user.
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Help to operate app", command=on_help)
    helpmenu.add_command(label="About us", command=lambda: print("K"))
    menubar.add_cascade(label="Help", menu=helpmenu)
    # Theme options menu design and call change theme fuction if any option is pressed
    thememenu = Menu(menubar, tearoff=0)
    thememenu.add_command(label="Light theme", command=lambda: change_theme(theme['white_theme']))
    thememenu.add_command(label="Dark theme", command=lambda: change_theme(theme['black_theme']))
    thememenu.add_command(label="Warm theme", command=lambda: change_theme(theme['orange_theme']))
    thememenu.add_command(label="Cool theme", command=lambda: change_theme(theme['blue_theme']))
    menubar.add_cascade(label="Theme", menu=thememenu)
    # Put default settings to main window
    root.configure(background=cur_theme['app-bg'], pady=10, padx=10, menu=menubar)
    # Start app now.
    root.mainloop()



#     to_input  +'@gmail.com'
# to = to_gmail_spaced.replace(" ", "").replace('dot','.').lower()
# print(to)