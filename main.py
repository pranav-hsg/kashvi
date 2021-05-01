import speech_recognition as sr
from gtts import gTTS
import pyautogui
import datetime
import requests
import json
import re
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
    error_dict = {
        1: tk.messagebox.showinfo,
        2: tk.messagebox.showwarning,
        3: tk.messagebox.showerror
    }
    error_func = error_dict.get(choice, " ")
    # text_translator(title, lang["display-text"]), text_translator(body, lang["display-text"])
    error_func(title,body)


icon = {
    "error": "images/err.ico",
    "message": "images/msg.ico",
    "tkinter-title-icon": "images/assistant.png",
}

sender_email_info = {
    'user_name': 'superfighterpr@gmail.com',
    'user_password': ''
}
lang = {
    'display-text': 'en',
    'input-speech': 'kn',
    'output-speech': 'kn',
}
api_keys = {
    'news_api': os.getenv('newsapi_api_key'),
    'weather_api' : os.getenv('weather_api_key')
}
error_codes  = {
    'internet-error': {
        'etks':1000,
        'newsteller':1001,
        'weather-report':1003,
    },
    'unknown-error': {
        'newsteller':1004,
        'notification':1005,
        'weather-report':1006,
    },
    'dir-error':{
        'dir':1007,
    },
    'whatsapp':{
        'msg-error':1008,
    },
    'power':{
        'tweak-power':1009,
    }

}
# Array of bad words
bad_words = ['ಮುಕುಳಿ', 'ಕೆಯ', 'ನಾಯಿ ಕತ್ತೆ', 'ತುಲ್ಲೇ', 'ತುಲ್ಲಗ್', 'ತುಲ್ಲ', 'ತುನ್ನಿ', 'ಬೋಸುಡಿ', 'ಬೆವರ್ಸಿ', 'ಹಡ್ಬೆ',
             'ಸೂಳೇ',
             'ಸಾಟ', 'ಶಾಟ', 'ಹಲ್ಕಟ್', 'ಅಲ್ಕಟ್', 'ಹಲ್ಕಾಟ್', 'ಮಿಂಡ್ರೀ', 'ಮಿಂಡಾ', 'ಬಡ್ಡಿ', 'ಮುಂಡೆ', 'ಫಕ್', 'ಲೋಫರ್',
             'ನಿಮ್ಮಜ್ಜಿ', 'ಕತ್ತೆ', 'ಮಂಗ', 'ಸುವರ್', 'ಗಂಜರ್', 'ಬಿಚ್', 'ಪೀಸ್', 'ಬ್ಲಡಿ', 'ಹೆಲ್', 'ನಾಯಿ', 'ವಡ್ಡ']


# Tests if any of the array of words is present in given line
def testifarrayinline(arr, line):
    for elem in arr:
        # if elem in line:
        if re.search(elem, line):
            return True
    return False


def return_searched_word(arr, line):
    for elem in arr:
        # if elem in line:
        if re.search(elem, line):
            return elem
    return False


# def clear_screen():
#     os.system(‘cls’)


# def send_email(reciever_email='pranavprati@gmail.com', reciever_content='This is it'):
#     server = smtplib.SMTP('smtp.gmail.com',587)
#     server.ehlo()
#     server.starttls()
#     server.login(sender_email_info['user_name'], sender_email_info['user_password'])
#     server.sendmail('youremail@gmail.com', reciever_email,reciever_content)
#     server.close()
# send_email()
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
        print("Say that again please...", e)
        display("Say that again please...", 2)
        etks("Please say that again when i am listening")
        return None
    return query


# Open website function
def open_website(website, new_tab=0):
    try:
        webbrowser.open_new(website)
    except Exception as e:
        print("Error while opening website [open_website]"+e)


# Playing music function
def say(music):
    playsound(music);


# English to Kannada or vice versa text function
def text_translator(text, dest='kn'):
    try:
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
    # print("No")
    # say("eng.mp3")
    # time.sleep(.5)
    # say("eng.mp3")


# News speaking function
def newsteller(number=10, country='in', category='&category=business', q='&q=tesla'):
    x = []
    api_key = api_keys['news_api']
    url = f'https://newsapi.org/v2/top-headlines?country={country}&language=en&apiKey={api_key}'
    try:
        x = requests.get(url, timeout=5)
        x = json.loads(x.text)
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("Internet problem occurred inside [newsteller]")
        error_message(f"Error e[{error_codes['internet-error']['newsteller']}]", 'No Internet for fetching News', 3)
    counter = 0
    try:
        if len(x) != 0:
            for id, cray in enumerate(x['articles']):
                counter += 1
                if counter > int(number):
                    break
                regexp = '.*\s-\s'
                pattern = re.compile(r'.*\s-\s')
                result = re.search(pattern, cray['title'])
                etks(f"News number {id + 1}")
                etks(result.group(), id)
            # print(result.group(), id)
    except Exception as e:
        print("Error occurred inside [newsteller] :", e)
        error_message(f"Error e[{error_codes['unknown-error']['newsteller']}]",e, 3)


# Wish according to time function
def wish_time(time=datetime.datetime.now().strftime("%H")):
    time = int(time)
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


def create_dir(dir_array):
    for dir in dir_array:
        if not (path.exists(dir)):
            try:
                os.mkdir(dir)
            except Exception as e:
                print("Not able to make music directory inside [create_dir] :", e)
                error_message(f"Error e[{error_codes['dir-error']['dir']}]", 'Not able to make directory', 3)

def clear_dir(dir_array):
    for dir in dir_array:
        if path.exists(dir):
            try:
                filelist = [f for f in os.listdir(dir)]
                for f in filelist:
                    os.remove(os.path.join(dir, f))
            except Exception as e:
                print("Not able to make music directory inside [clear_dir] :", e)
                error_message(f"Error e[{error_codes['dir-error']['dir']}]", 'Not able to make directory', 3)


# Initialization function
def init():
    if not (path.exists("music")):
        try:
            os.mkdir("music")
        except Exception as e:
            print("Not able to make music directory inside [init] :", e)
            error_message(f"Error e[{error_codes['dir-error']['dir']}]", 'Not able to make directory', 3)
    wish_time()
    ggap()
    etks("I am kashvi,please tell me how may i help", 1)


# Send whats app message function
def swm(msg, num):
    try:
        hr = int(datetime.datetime.now().strftime("%H"))
        mn = int(datetime.datetime.now().strftime("%M")) + 1
        sec = int(datetime.datetime.now().strftime("%S"))
        print(sec)
        print(mn)
        if sec > 30:
            mn = mn + 1
        pywhatkit.sendwhatmsg('+91' + num, msg, hr, mn)
    except:
        print("Message can't be sent in [swm]",e)
        error_message(f"Error e[{error_codes['whatsapp']['msg-error']}]", 'An error while sending message', 3)



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
    # strptime function parses string
    cur_time = datetime.datetime.strptime(local_time, '%a %b %y %H:%M:%S %Y')
    return cur_time


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
            sunRiseInfo = f"Expected sunrise {str(sunRiseTime.hour) + ':' + str(sunRiseTime.minute)}"
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
        print('Error occurred',e)
        # "ಕ್ಷಮಿಸಿ ಯಾವುದೇ ಮಾಹಿತಿ ಇಲ್ಲ"

        etks("Sorry there is no information")


commands = {
    'time': ['ಟೈಮ್', 'ಟೈಮ್ ಎಷ್ಟು', 'ಗಂಟೆ ಎಷ್ಟು', 'ಟೈಮೆಷ್ಟು', 'ಸಮಯ ಎಷ್ಟು', 'ಸಮಯವೆಷ್ಟು'],
    'news': ['ವಾರ್ತೆ ತಿಳಿಸು', 'ನ್ಯೂಸ್ ತಿಳಿಸು', 'ಮುಖ್ಯ ವಾರ್ತೆ ತಿಳಿಸು', 'ಸುದ್ದಿ ತಿಳಿಸು'],
    'wikipedia': ['ವಿಕಿಪೇಡಿಯ', 'ವಿಕಿಪಿಡಿಯಾ', 'ವಿಕಿಪೀಡಿಯ'],
    'you-tube': ['ಯೂಟ್ಯೂಬ್ ಅನ್ನು ತೆರೆಯಿರಿ', 'ಯೂಟ್ಯೂಬ್ ತೆರೆ', 'ಯುಟ್ಯೂಬ ಓಪನ್', 'ಓಪನ್ ಯುಟ್ಯೂಬ', 'ಓಪನ್ ಯುಟ್ಯೂಬ್',
                 'ಯುಟ್ಯೂಬ್ '],
    'google': ['ಗೂಗಲ್ ಅನ್ನು ತೆರೆಯಿರಿ', 'ಗೂಗಲ್ ತೆರೆ', 'ಗೂಗಲ್ ಓಪನ್', 'ಓಪನ್ ಗೂಗಲ್'],
    'weather': ['ವೆದರ್', 'ಹವಾಮಾನ', 'ವಾತಾವರಣ'],
    'whatsapp': ['ವಾಟ್ಸಪ್', 'ವಾಟ್ಸಾಪ್'],
    'restart': ['ರೀಸ್ಟಾರ್ಟ್ ಕಂಪ್ಯೂಟರ್', 'ಗಣಕಯಂತ್ರವನ್ನು ಮರು ಪ್ರಾರಂಭಿಸು', 'ಗಣಕಯಂತ್ರವನ್ನು ಮರುಪ್ರಾರಂಭಿಸಿ'],
    'sleep': ['ಗಣಕಯಂತ್ರವನ್ನು ಮಲಗಿಸು', 'ಗಣಕಯಂತ್ರ ಮಲಗು', 'ಸ್ಲೀಪ್ ಕಂಪ್ಯೂಟರ್', 'ಕಂಪ್ಯೂಟರ್ ಸ್ಲೀಪ್', 'ಮುಚ್ಕೋ ಮಲ್ಕ',
              'ಮುಚ್ಕೊಂಡ್ ಮಲ್ಕೋ', 'ಮುಚ್ಕೊಂಡು ಮಲ್ಕ'],
    'power-off': ['ಕಂಪ್ಯೂಟರ್ ಕೆಡಿಸು', 'ಕಂಪ್ಯೂಟರ್ ಆರಿಸು', 'ಗಣಕಯಂತ್ರವನ್ನು ಆರಿಸು', 'ಗಣಕಯಂತ್ರವನ್ನು ಕೆಡಿಸು',
                  'ಶಟ್ ಡೌನ್ ಕಂಪ್ಯೂಟರ್', 'ಕಂಪ್ಯೂಟರ್ ಶಬ್ದೊನ್', 'ಕಂಪ್ಯೂಟರನ್ನು ಆರಿಸು'],
    'google-text': ['ಗೂಗಲ್', 'ಗೋಗಲ್', 'ಗಾಗಲ್'],
    'map': ['ಮ್ಯಾಪ್','ಮ್ಯಾಪ್ಸ್','ನಕ್ಷೆ'],
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
        etks(f"Some error has occurred")
        error_message(f"Error e[{error_codes['power']['tweak-power']}]", 'Some error occured while tweaking power', 3)
        print(e)


def google_search(user_input="who is Prime Minister of India"):
    #Meaning of the word
    if testifarrayinline(commands['meaning'], user_input):
        print("If passed")
        query = user_input.replace(return_searched_word(commands['meaning'], user_input), '')
        english_query = text_translator(query,'en')
        print(english_query)
        apended_eng_query = 'meaning of the word '+ english_query
        print(apended_eng_query,type(apended_eng_query ))
        result = requests.get(f"https://www.google.com/search?q={apended_eng_query}")
        html_text = result.text
        html_parsed = BeautifulSoup(html_text, 'html.parser')
        # print(html_parsed.prettify())
        # print(html_parsed)
        match = html_parsed.find_all("div", {"class": "BNeawe s3v9rd AP7Wnd"})[2]

        # match = html_parsed.find_all('div', {"data-dobid" : "dfn"})
        # print(match.prettify())
        # print(match.text)
        print(match.text)
        etks(match.text)
    else:
        user_input = text_translator(user_input, dest='en')
        result = requests.get(f"https://www.google.com/search?q={user_input}")
        html_text = result.text
        html_parsed = BeautifulSoup(html_text, 'html.parser')
        match = html_parsed.find('div', class_='BNeawe')
        # print(match.text.split(".", 1))
        etks(match.text)


# Opens google maps using selenium tool
def open_google_maps(url):
    # Here Chrome  will be used
    global driver
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

def main():
    # Taking user input in kannada language
    user_input = takeuserinput()
    # Take user input until he/she speaks something
    while user_input is None:
        user_input = takeuserinput()
    # Only enter function if user input is not none
    if (user_input is not None) and (user_input != 'None'):
        # Checks for bad words
        bwc(user_input)
        # If user asks for time
        if testifarrayinline(commands['time'], user_input):
            curtime()
        # If user asks for news
        elif testifarrayinline(commands['news'], user_input):
            etks("How many news do you want to hear")
            newsteller(takeuserinput('en', "Tell me how many news do you want to hear...."))
        # If user asks for wikipedia search
        elif testifarrayinline(commands['wikipedia'], user_input):
            wikiQuery = user_input.replace(return_searched_word(commands['wikipedia'], user_input), '')
            wikipedia_search(wikiQuery)
        # If user asks to open you tube browser
        elif testifarrayinline(commands['you-tube'], user_input):
            map_query = user_input.replace(return_searched_word(commands['you-tube'], user_input), '')
            open_website("https://www.youtube.com/f{}")
        # If user asks to open google in browser
        elif testifarrayinline(commands['google'], user_input):
            open_website("https://www.google.com")
        # If user asks for weather data
        elif testifarrayinline(commands['weather'], user_input):
            weather_report()
        # If user asks for message using whatsapp
        elif testifarrayinline(commands['whatsapp'], user_input):
            try:
                message = takeuserinput('kn', 'Listening to message')
                number = takeuserinput('en')
                notify_system("ವಾಟ್ಸಪ್ ಸಂದೇಶ ಕಳುಹಿಸುವ ಪ್ರಕ್ರಿಯೆ ಪ್ರಾರಂಭವಾಗಿದೆ",
                              '"' + message + ' "ಎಂಬ ಸಂದೇಶವನ್ನು ' + number + 'ಗೆ ಕಳುಹಿಸಲಾಗುವುದು', icon['message'], 10)
                swm(message, number)
            except Exception as e:
                print("Inside main in whatsapp",e)

        elif testifarrayinline(commands['power-off'], user_input):
            # Power off fucntion
            tweak_power("shutdown /s /t 1", 'power-off')
        elif testifarrayinline(commands['restart'], user_input):
            # Restart fucntion
            tweak_power("shutdown /r /t 1", 'restart')
        elif testifarrayinline(commands['sleep'], user_input):
            # Sleep function
            tweak_power("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", 'sleep')
        elif testifarrayinline(commands['google-text'], user_input):
            # Google function
            google_query = user_input.replace(return_searched_word(commands['google-text'], user_input), '')
            google_search(google_query)
        elif testifarrayinline(commands['map'], user_input):
            # Google map function
            map_query = user_input.replace(return_searched_word(commands['map'], user_input), '')
            # map_query = text_translator(map_query,'en')
            open_google_maps(f"https://www.google.com/maps/place/{map_query}")
        else:
            etks("Sorry I am not able to hear because of combined voice")
    main()


####################################################################################
# ----------------------------------- GUI DESIGN --------------------------------- #
####################################################################################


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


def on_start():
    create_dir(['music','images','help','data'])
    display("Started", 1)
    clear_display(heading_text1, heading_text2, main_screen_text)
    global t1, is_alive
    if t1 is None:
        t1 = thread_with_exception(main, main)
        t1.daemon = True
        t1.start()
        is_alive = True
    elif t1 is not None:
        if not is_alive:
            t1 = thread_with_exception(main, main)
            t1.daemon = True
            t1.start()
            is_alive = True
        else:
            error_message("Warning", "App is already started", 2)


def on_stop():
    clear_dir(['music'])
    clear_display(heading_text1, heading_text2, main_screen_text)
    display("App has Stopped,Press start", 1)
    display("Stopped", 2)
    display("Press start to start the program",4)
    global t1, is_alive
    if is_alive:
        if t1 is not None:
            is_alive = False
            t1.raise_exception()
            t1 = None
    else:
        error_message("Warning", "App is already stopped", 2)


def on_restart():
    on_stop()
    on_start()
    display("Restarted", 1)


def clear_display(*args):
    for elem in args:
        elem.set("")


def on_clear():
    clear_display(heading_text1, main_screen_text)


def display(value, choice):
    func_switcher = {
        1: notify_heading_text,
        2: heading_text1,
        3: heading_text2,
        4: main_screen_text,
    }
    disp_func = func_switcher.get(choice, " ")
    text_switcher = {
        1: "App has ",
        2: "Condition  :",
        3: "Input   : ",
        4: "Output  : ",
    }
    disp_text = text_switcher.get(choice, " ")
    disp_func.set(disp_text + value)


def timeout(sec, func):
    root.after(sec, func)


def hello(a="a"):
    pyautogui.press("mute")
    # for _ in range(50):
    #     pyautogui.press("volumeup")


def tweak_volume(volume_points, volume_up=True):
    if volume_up:
        for _ in range(volume_points):
            pyautogui.press("volumeup")
    else:
        for _ in range(volume_points):
            pyautogui.press("volumedown")


def on_help():
    path = os.getcwd()
    path_of_file = os.path.join(path, 'help/help.txt')
    os.startfile(path_of_file, 'open')


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
# ededed
cur_theme = theme['black_theme']


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


from pathlib import Path

if __name__ == '__main__':
    # global variables
    # t1 is thread one which is used to start or stop a thread
    t1 = None
    # is_alive is used to check is thread dead if it is alive then block start
    is_alive = False
    root = Tk()
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
    root.minsize(400, 600)
    # root.maxsize(401, 601)
    main_screen_text = tk.StringVar()
    heading_text1 = tk.StringVar()
    heading_text2 = tk.StringVar()
    notify_heading_text = tk.StringVar()

    out_txt = "Press Start to Start program"
    notification1 = Label(height=1, textvariable=notify_heading_text, bd=0)
    notification1.pack(fill=X, side=TOP)
    notification1.configure(bg=cur_theme['app-bg'], fg=cur_theme['n1-txt'], font=('Helvetica', 12, 'bold'), pady=10)

    heading1 = Label(height=1, wraplength=380, textvariable=heading_text1, bd=0)
    heading1.pack(fill=X, side=TOP)
    heading1.configure(bg=cur_theme['app-disp-bg'], fg=cur_theme['h1-txt'], font=('Helvetica', 16, 'bold'), pady=10)

    heading2 = Label(height=2, wraplength=380, textvariable=heading_text2, bd=0)
    heading2.pack(fill=X, side=TOP)
    heading2.configure(bg=cur_theme['app-disp-bg'], fg=cur_theme['h2-txt'], font=('Helvetica', 12, 'bold'), pady=10)

    main_screen = Label(height=14, wraplength=380, textvariable=main_screen_text, bd=0)
    main_screen.pack(fill=BOTH, side=TOP, expand=TRUE)
    main_screen.configure(bg=cur_theme['app-disp-bg'], fg=cur_theme['main-txt'], font=('Helvetica', 12, 'bold'),
                          pady=10)

    main_screen_text.set(out_txt)
    display("Stopped", 2)

    display("Stopped , Press Start", 1)
    # notify('Started')
    start_btn_txt = tk.StringVar()
    start_btn = Button(root, borderwidth=0, fg=cur_theme['btn']['start-fg'], activebackground='#025aa5',
                       activeforeground='white',
                       bg=cur_theme['btn']['start-bg'], textvariable=start_btn_txt, command=on_start,
                       font=('Helvetica', 12, 'bold'), padx=10, pady=6, )
    start_btn_txt.set('Start')
    start_btn.pack(side=LEFT)

    stop_btn_txt = tk.StringVar()
    stop_btn = Button(root, borderwidth=0, fg=cur_theme['btn']['stop-fg'], activebackground='#ed0202',
                      activeforeground='white', bg=cur_theme['btn']['stop-bg'],
                      textvariable=stop_btn_txt, command=on_stop, font=('Helvetica', 12, 'bold'), padx=10, pady=6)
    stop_btn_txt.set('Stop')
    stop_btn.pack(side=LEFT, padx=90, pady=10)

    restart_btn_txt = tk.StringVar()
    restart_btn = Button(root, borderwidth=0, fg=cur_theme['btn']['rstart-fg'], activebackground='#40556a',
                         activeforeground='white', bg=cur_theme['btn']['rstart-bg'],
                         textvariable=restart_btn_txt, command=on_restart, font=('Helvetica', 12, 'bold'), padx=10,
                         pady=6)
    restart_btn_txt.set('Restart')
    restart_btn.pack(side=RIGHT)

    menubar = Menu(root, relief=FLAT, bd=0)

    # Sets menubar background color and active select but does not remove 3d  effect/padding

    # First item on menubar and creates sub options
    appmenu = Menu(menubar, tearoff=0)
    # # filemenu.config(bg="#5c5c5c")
    # filemenu["borderwidth"] = 0
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

    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Help to operate app", command=on_help)
    helpmenu.add_command(label="About us", command=lambda: hello("Args"))
    menubar.add_cascade(label="Help", menu=helpmenu)

    thememenu = Menu(menubar, tearoff=0)
    thememenu.add_command(label="Light theme", command=lambda: change_theme(theme['white_theme']))
    thememenu.add_command(label="Dark theme", command=lambda: change_theme(theme['black_theme']))
    thememenu.add_command(label="Warm theme", command=lambda: change_theme(theme['orange_theme']))
    thememenu.add_command(label="Cool theme", command=lambda: change_theme(theme['blue_theme']))
    menubar.add_cascade(label="Theme", menu=thememenu)

    root.configure(background=cur_theme['app-bg'], pady=10, padx=10, menu=menubar)

    root.mainloop()
