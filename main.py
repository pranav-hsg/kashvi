import speech_recognition as sr
import data as dt
from gtts import gTTS
import pyautogui
import datetime
import requests
import json
from apiclient.discovery import build
try:
    import pywhatkit
except Exception as e:
    print(e)
from pathlib import Path
import re
import smtplib
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
from tkinter import messagebox,font
import ctypes
import threading
import random
import itertools
try:
    from plyer import notification
except Exception as e:
    print(e)

# importing web driver from selenium
from selenium import webdriver


def error_message(title, body, choice):
    """
        The function to open info/warning/error window
        Parameters:
            title (str): The title of the error message.
            body (str): Description of error message.
            choice (int): Type of message ,1 ->info,2 -> warning,3 -> error
    """
    # using switch like statement
    error_dict = {
        1: tk.messagebox.showinfo,
        2: tk.messagebox.showwarning,
        3: tk.messagebox.showerror
    }
    error_func = error_dict.get(choice, " ")
    # text_translator(title, lang["display-text"]), text_translator(body, lang["display-text"])
    error_func(title, body)


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
    'user_name': 'superfighterpr@gmail.com',
    'user_password': os.getenv('device_mail_id')
}
# os.getenv('device_mail_id')
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

# api_keys = {
#     'news_api':1,
#     'weather_api' : 2,
#     'youtube_api':3
# }
api_keys = {
    'news_api': os.getenv('newsapi_api_key'),
    'weather_api': os.getenv('weather_api_key'),
    'youtube_api': os.getenv('youtube_api_key')
}

# Retrieving main data required for program from files inside data folder.
b_w = dt.retrieve_json_files(['bw.json'])[0][0]
theme = dt.retrieve_json_files(['theme.json'])[0][0]
commands = dt.retrieve_json_files(['commands.json'])[0][0]
error_codes = dt.retrieve_json_files(['errorcodes.json'])[0][0]


#  Error handling decorator
def handle_error(callback_func):
    def decorator_function(*args, **kwargs):
        non_notify = ['cur_time']
        try:
            result = callback_func(*args)
        except (requests.ConnectionError, requests.Timeout) as exception:
            print("Internet problem occurred while fetching data")
            error_message(f"Error occurred inside e[{callback_func.__name__}]",
                          'Error Details: \n' + 'Internet problem occurred while fetching data', 3)
        except Exception as e:
            result = ''
            print(f"Error occurred inside [" + callback_func.__name__ + "]")
            error_message(f"Error occurred inside e[{callback_func.__name__}]",'Error Details: \n'+str(e).capitalize(), 3)
            if  callback_func.__name__=='text_translator':
                result="Sorry error occurred while text translation"
            if callback_func.__name__=='takeuserinput':
                on_stop()
        else:
            if callback_func.__name__ == 'send_mail' or callback_func.__name__ == 'swm':
                display('Successfully sent message', 4)
                etks("Message has been sent successfully")
            if callback_func.__name__  in non_notify:
                print("Task done successful")
                print(callback_func.__name__)
                notify_system("Success",
                              'Task Successfully done',
                              icon["message"], 8)
            return result
        return result

    return decorator_function


def run_async(callback_func):
    def decorator_function(*args, **kwargs):
        try:
            t1 = threading.Thread(target=etks, args=("Information is being fetched from the Internet,please wait for a while",))
            t1.start()
            result = callback_func(*args)
            t1.join()
            return result
        except:
            return ''
    return decorator_function

# Tests if any of the array of words is present in given line
@handle_error
def testifarrayinline(arr, line):
    """
        The function to return if keyword in array(arr) is contained in input String(line).
        Parameters:
            arr (list): The list which contains commands.
            line (str): User given input string line.
        Returns:
            bool: Returns True or False.
    """
    # It takes array of string and string line,
    # for every string in array put the string to elem
    for elem in arr:
        # if elem in line:
        if re.search(fr'({elem}+\s)|({elem}$)', line):
            return True
    return False


@handle_error
def remove_special_charecters(string, regexp='[^A-Za-z0-9\s]+', replace_many_space_with_onespace=True):
    # Filter special charecters according to reg exp
    # By default  it filters everything except alphabets,digits,spaces
    clean_string = re.sub(regexp, '', string)
    # If true return replace all multiple spaces with one space and return it
    if replace_many_space_with_onespace: return ' '.join(clean_string.split())
    # else return clean string
    return clean_string


@handle_error
def return_searched_word(arr, line):
    """
        The function to return if keyword in array(arr) is contained in input String(line).
        Parameters:
            arr (list): The list which contains commands.
            line (str): User given input string line.
        Returns:
            str: Returns None or searched keyword element in command array.
    """
    # It takes array of string and string line,
    # for every string in array put the string to elem
    for elem in arr:
        # if elem is in line:
        # re.search(elem, line)

        if re.search(fr'({elem}+\s)|({elem}$)', line):
            return elem
    return ''


@handle_error
def send_mail():
    """
        The function to send email which accepts no input.
    """
    from_mail = sender_email_info['user_name']
    frommail_password = sender_email_info['user_password']
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
    notify_system("ಸಂದೇಶ ಕಳುಹಿಸುವ ಪ್ರಕ್ರಿಯೆ ಪ್ರಾರಂಭವಾಗಿದೆ", to_mail + 'ಗೆ ಕಳುಹಿಸಲಾಗುವುದು', icon['message'], 10)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(from_mail, frommail_password)
    server.sendmail(from_mail, to_mail, content)
    server.close()
    return True
    # mxsxmvkvdkvirtul


# This function accepts a command from the user in speech form
@handle_error
def takeuserinput(lang='kn', msg='Listening...'):
    """
        The function which accepts input in the form of audio from the user.
        Parameters:
            lang (str): Name of the input language to accept,ex : 'en' for English.
            msg (str): To display to user while accepting command like 'Listening...'.
        Returns:
            str: Returns input in the form of string which is accepted from user.
    """
    # It takes microphone input from the user and returns string output
    with sr.Microphone() as source:
        r = sr.Recognizer()
        print(msg)
        display(msg, 2)
        # hear=True
        r.pause_threshold = 0.6
        audio = r.listen(source)

        try:
            # query = ret_rand_cmd()
            display("Recognizing......", 2)
            print("Recognizing...")
            query = r.recognize_google(audio, language=f'{lang}-IN')
            clear_display(heading_text1)
            display("Processing...", 2)
            display(query, 3)
            print(f"User said: {query}\n")

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
@handle_error
def open_website(url, new_tab=0):
    """
        The function which opens a url in default browser.
        Parameters:
            url (str): Url of the website to open.
            new_tab (int): If one wants to open in new tab or not.
    """
    webbrowser.open_new(url)


# Playing music function
@handle_error
def say(music):
    """
        The function which plays music synchronously.
        Parameters:
            music (str): path to music file and its name at end of path.
    """
    # Use playsound and not play using os module because playsound plays syncronously while
    # play using os module plays async leading to misbehaving of current app
    playsound(music)


# English to Kannada or vice versa text function
@handle_error
def text_translator(text,dest='kn'):
    """
        The function translates text.
        Parameters:
            text (str): Text to be converted.
            dest (str): Destination language to be converted.
        Returns:
            str : Translated text in the form of string.
    """
    # if Translator().translate('ಹೌದು', dest='en').text in 'yes Yes':
    try:
        translator = Translator()
        translation = translator.translate(text, dest=dest)
        translate_text = translation.text
        return translate_text
    except:
        print("Second translator is used as fallback")
        from google_trans_new import google_translator
        translator = google_translator()
        translate_text = translator.translate(text, lang_tgt=dest)
        return translate_text


# English text to kannada speech function
@handle_error
def etks(text, id=1):
    """
        The function converts english language text to kannada language speech.
        Parameters:
            text (str): Text to be converted to speech.
            id (int): To set music id (Not important).
    """
    dir = f"music//eng{id}.mp3"
    kan_txt = text_translator(text, 'kn')
    # gui.heading_display(kan_txt)
    display(kan_txt, 4)
    print(kan_txt)
    obj = gTTS(text=kan_txt, slow=False, lang='kn')
    obj.save(dir)
    say(dir)
    os.remove(dir)
    # except Exception as e:
    # error_message(f"Error e[{error_codes['internet-error']['etks']}]",'No Internet for text translation',3)
    # print("No Internet for text translation and speech in [etks] :", e)


# News speaking function
@handle_error
def newsretriever(number=10, api_key=api_keys['news_api'], country='in', category='&category=business', q='&q=tesla'):
    """
        The function which speaks news.
        Parameters:
            number (int): Number of news to tell.
            country (str): Country of which to tell news.
            :param api_key: Api key
    """
    x = []
    counter = 0
    # Number of news
    news_list = []
    url = f'https://newsapi.org/v2/top-headlines?country={country}&language=en&apiKey={api_key}'
    x = requests.get(url, timeout=5)
    # parse and get json from response
    x = json.loads(x.text)
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
            result = re.search(pattern, cray['title']).group()
            clean_result = remove_special_charecters(result)
            news_list.append(clean_result)
        return news_list



# Wish according to time function
@handle_error
def wish_time(hour=datetime.datetime.now().strftime("%H")):
    """
        The function to wish time,like 'good morning'.
        Parameters:
            hour (Any): Optional time input to speak.
    """
    # convert string time to int type
    hour = int(hour)
    # these are self explanatory
    if 5 < hour < 12:return "Good morning"
    elif 12 <= hour < 17:return "Good Midday"
    elif 17 <= hour < 19:return "Good Evening"
    else:return "Good Night"


# Bad word checker function
@handle_error
def bwc(cmd):
    for bw in b_w:
        # if bw in cmd:
        if bw in cmd:
            # ಇದುನ್ನಾ ನಿನ್ನ ಅಪ್ಪಂಗೆ ಹೇಳು
            return bw
    return ""


# Current time enquiry function
@handle_error
def curtime():
    """
        The function speaks current time (hour and minutes)
    """
    # ex:returns as 13 : 07
    return datetime.datetime.now().strftime("%H : %M ")


# Give gap function
@handle_error
def ggap(tim=0.5):
    """
        The function which is shorthand for time.sleep function (Blocks code for user specified time).
        Parameters:
            tim (float): Optional time in seconds to stop.
    """
    time.sleep(tim)


# fuction to create a directory,this function creates all dirs in dir_array
@handle_error
def create_dir(dir_array):
    """
        The function which creates directories in given array.
        Parameters:
            dir_array (list): An array of directory names to create.
    """
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
@handle_error
def clear_dir(dir_array):
    """
        The function which clears all files and directories inside a given directory array.
        Parameters:
            dir_array (list): An array of directory names to clear.
    """
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
@handle_error
def init():
    etks(wish_time())
    ggap()
    etks("I am kashvi,please tell me how may i help", 1)


# Send whats app message function
@handle_error
def swm():
    """
        The function sends whatsapp message.
    """
    etks("Speak the message you want to send when I start to listen")
    # Calculate current time hour,min,sec
    ggap()
    msg = takeuserinput('kn', 'Listening to message')
    etks("Enter the number to which you want to send a whatsapp message")
    # Take number to which user wants to send message
    display('Enter the target number to which you want to send whatsapp message and then press submit', 4)
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


# Notification function to show notification to system
# @handle_error
def notify_system(title, message, app_icon, timeout=4):
    """
        The function which pops system notification.
        Parameters:
            title (str): Title to display in notification.
            message (str): Message to display notification.
            app_icon (str): Path of icon to display in notification.
            timeout (int): Number of seconds until notification vanishes.
    """
    try:
        notification.notify(
            title=title,
            message=message,
            app_icon=app_icon,
            timeout=timeout,
            toast=False
        )
    except Exception as e:
        print("Notify error")


@handle_error
def utc_to_time(secsTillEpoch):
    """
        The function converts seconds till Epoch to hours and minutes and date,ex 1618965725 -> Wed Apr 21 06:12:05 2021.
        Epoch (or Unix time or POSIX time or Unix timestamp) is the number of seconds that have elapsed since January 1,
        1970 (midnight UTC/GMT), not counting leap seconds.
        Parameters:
            secsTillEpoch (int): Seconds till Epoch.
        Returns:
            datetime: Returns parsed date and time in the format of '%a %b %d %H:%M:%S %Y'.
    """
    # ctime converts epoch to string ex:1618965725 -> Wed Apr 21 06:12:05 2021
    local_time = time.ctime(secsTillEpoch)
    # strptime function parses from string
    cur_time = datetime.datetime.strptime(local_time, '%a %b %d %H:%M:%S %Y')
    return cur_time


# Enter latitude and longitude to get weather information
@run_async
@handle_error
def weather_report(latitude=13.66675, longitude=75.30914, api_key=api_keys['weather_api']):
    """
        The function speaks weather report with help of etks function.
        Parameters:
            latitude (int): Latitude of the area of which you want to fetch weather.
            longitude (int): Longitude of the area of which you want to fetch weather.
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid" \
          f"={api_key}&lang=en "
    json_object = {}
    w = {}
    json_object = json.loads(requests.get(url).text)
    w = json_object
    json_formatted_str = json.dumps(json_object, indent=2)
    # Check if dictionary is empty
    if len(w) != 0:
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
        temperatureInfo = f"  Temperature is {round(w['main']['temp'] - 273.1, 2)} degree Celsius .It is feeling like {round(w['main']['feels_like'] - 273.15, 2)} degree Celsius."
        # Information about pressure in pascal
        pressureInfo = f"  Pressure is {w['main']['pressure'] * 100} Pascal."
        # Information about humidity in percentage
        humidityInfo = f"  Humidity is {w['main']['humidity']}%."
        # Information of sunrise
        sunRiseInfo = f"Expected sunrise {str(sunRiseTime.hour)} hour and {str(sunRiseTime.minute)} minute"
        # Information of sunset
        sunSetInfo = f"Expected sunset {str(sunSetTime.hour - 12)} hour and {str(sunSetTime.minute)} minute"
        # Speak all info through etks function
        return windInfo + weatherInfo + temperatureInfo + pressureInfo + humidityInfo + sunRiseInfo + sunSetInfo

@run_async
@handle_error
def wikipedia_search(query, sentences=2):
    """
        The function speaks data from wikipedia with the help of etks.
        Parameters:
            query (str): Search string to query.
            sentences (int): Number of sentences to fetch.
    """
    print(query)
    result = wikipedia.summary(query, sentences=sentences)
    print("result:", result)
    return remove_special_charecters(result)


@handle_error
def ret_rand_cmd():
    random_element = random.choice(list(commands.values()))
    cmd = random.choice(random_element)
    print(cmd)
    return cmd


@handle_error
def tweak_power(command, action):
    """
        The function executes given command( such as tweaking power).
        Parameters:
            command (str): Command to take action.
            action (str): Action to make such as sleep/restart/power-off.
    """
    etks(f"Are you sure want to {action} computer")
    # Ask for user confirmation
    if testifarrayinline(commands['positive-statements'], takeuserinput('kn')):
        etks(f"Now computer will {action}")
        os.system(command)
    else:
        etks(f"Computer will not {action} due to your action or inaction")
    # If error occurs then


@handle_error
def google_search(user_input="who is Prime Minister of India"):
    """
        The function speaks data from google with the help of etks.
        Parameters:
            user_input (str): Query to search in google.
    """
    # if user wanted to search Meaning of the word
    if testifarrayinline(commands['meaning'], user_input):
        # replace words in commands['meaning'] array with ''
        query = user_input.replace(return_searched_word(commands['meaning'], user_input), '')
        # Translate kannada query to english
        english_query = text_translator(query, 'en')
        # Append 'meaning of the word ' to get perfect search result
        apended_eng_query = 'meaning of the word ' + english_query
        # Request html data from this url
        result = requests.get(f"https://www.google.com/search?q={apended_eng_query}")
        html_text = result.text
        # Parse html data
        html_parsed = BeautifulSoup(html_text, 'html.parser')
        # Scrape html to find particular div which contains data using Beautiful soup
        # find_all finds all 'div' but [2] selects only third 'div'
        match = html_parsed.find_all("div", {"class": "BNeawe s3v9rd AP7Wnd"})[2]
        # speak result
        return match.text
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
        return match.text


# Get youtube link ,note that you want api key for youtube.
@handle_error
def get_youtube_link(query):
    """
        The function opens particular video in browser according to user query with the help of youtube api.
        Parameters:
            query (str): Search string to query.
    """
    youtube = build('youtube', 'v3', developerKey=api_keys['youtube_api'])
    # search you tube for top results
    req = youtube.search().list(q=query, part='snippet', type='video')
    # grab top result video id.(video id is unique id given to every video by you tube)
    video_id = req.execute()['items'][0]['id']['videoId']
    # form you tube link from video id
    youtube_link = f'https://www.youtube.com/watch?v={video_id}'
    return youtube_link


# Opens google maps using selenium tool
@handle_error
def open_google_maps(url):
    """
        The function opens google map according to user query.
        Parameters:
            url (str): url to fetch.
    """
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


@handle_error
def recursive_input(lang='kn'):
    """
        The function takes recursive input till user speaks.
        Parameters:
            lang (str): Name of the input language .
        Returns:
            str : returns query input.
    """
    # Taking user input in kannada language
    # User user_input is in the format of  kannada string
    user_input = takeuserinput()
    # Take user input until he/she speaks something
    while user_input is None:
        user_input = takeuserinput()
    # return user input
    return user_input


def is_valid(key,user_input):
    return testifarrayinline(commands[key], user_input)

count = 0
# Main function
@handle_error
def main(commands=commands):
    """
        This is the main function.
    """
    global count
    if count == 0:
        pass
        # init()
        # count+=1
    # Recursive input takes user from input until user speaks
    user_input = recursive_input('kn')
    # Only enter function if user input is not none
    if (user_input is not None) and (user_input != 'None'):
        # Checks for bad words
        bwc(user_input)
        # If user asks for time
        if is_valid('time',user_input):
            etks(curtime())
        # If user asks for news
        elif is_valid('news',user_input):
            # etks("How many news do you want to hear")
            print('How')
            # take user input('en', "Tell me how many news do you want to hear....")
            for news in newsretriever(2):
                etks(news)
        # If user asks for wikipedia search
        elif is_valid('wikipedia',user_input):
            wikiQueryKan = user_input.replace(return_searched_word(commands['wikipedia'], user_input),'')
            wikiQueryEng = text_translator(wikiQueryKan, 'en')
            result = wikipedia_search(wikiQueryEng)
            if result:
                etks("According to wikipedia")
                etks(result)
            else:
                etks("Sorry there is no information")
        # If user asks to open you tube browser
        elif is_valid('you-tube',user_input):
            yt_query = user_input.replace(return_searched_word(commands['you-tube'], user_input), '')
            open_website(get_youtube_link(text_translator(yt_query, 'kn')))
        # If user asks to open google in browser
        elif is_valid('google',user_input):
            open_website("https://www.google.com")
        # If user asks to open google in browser
        elif is_valid('twitter',user_input):
            open_website("https://twitter.com")
        # If user asks to open google in browser
        elif is_valid('facebook',user_input):
            open_website("https://www.facebook.com")
        # If user asks to open google in browser
        elif is_valid('instagram',user_input):
            open_website("https://www.instagram.com/")
        # If user asks for weather data
        elif is_valid('weather',user_input):
            result = weather_report()
            if result:
                etks(result)
            else:
                error_message(f"Error e[{error_codes['unknown-error']['weather-report']}]", e, 3)
        # If user asks for message using whatsapp
        elif is_valid('whatsapp',user_input):
            try:
                # call send whatsapp message
                swm()
            except Exception as e:
                print("Inside main in whatsapp", e)
        elif is_valid('e-mail',user_input):
            send_mail()
        # If user asks for computer operation like on,off,restart
        elif is_valid('power-off',user_input):
            # Power off fucntion
            tweak_power("shutdown /s /t 1", 'power-off')
        elif is_valid('restart',user_input):
            # Restart fucntion
            tweak_power("shutdown /r /t 1", 'restart')
        elif is_valid('sleep',user_input):
            # Sleep function
            tweak_power("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", 'sleep')
        # If user asks for Google search the given keyword
        elif is_valid('google-text',user_input):
            # Google function
            # replace function replaces first parameter with second parameter
            # return searched word returns exactly key word used by user to trigger this elif block
            google_query = user_input.replace(return_searched_word(commands['google-text'], user_input), '')
            display(text_translator("Information is being fetched please wait", 'kn'), 3)
            result = google_search(google_query)
            print(result)
            clean_result = remove_special_charecters(result)
            print(clean_result)
            if result:
                etks(clean_result)
            else:
                etks("Sorry some error occurred while fetching information")
                error_message(f"Error e[{error_codes['internet-error']['google-search']}]",
                              'Internet problem occurred while google search', 3)
        # If user asks for google map to show a village/city
        elif is_valid('map',user_input):
            # Google map function
            map_query = user_input.replace(return_searched_word(commands['map'], user_input), '')
            # map_query = text_translator(map_query,'en')
            open_google_maps(f"https://www.google.com/maps/place/{map_query}")
        else:
            pass
            # etks("Sorry I am not able to hear because of combined voice")
            # ggap(1)
    # call main function recursively until stop button is pressed in gui
    main()


####################################################################################
# ----------------------------------- GUI DESIGN --------------------------------- #
####################################################################################

# Thread class
class thread_with_exception(threading.Thread):
    """
       This is a class to stop thread.
   """
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
@handle_error
def on_start():
    """
        The function starts thread when start button is clicked.
    """
    # Clean music directory if app is not stopped properly last time
    clear_dir(['music'])
    # Grab global variables instead of function variables
    # If global is not specified function variables are called
    global t1, is_alive
    if not is_alive:
        # Create all directories required for entire app to avoid error
        create_dir(['music', 'images', 'help', 'data'])
        display("Started", 1)
        clear_display(heading_text1, heading_text2, main_screen_text)
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
    else:
        error_message("Warning", "App is already started", 2)


# When stop button is pressed
@handle_error
def on_stop():
    """
        The function stops thread when stop button is clicked.
    """
    # Grab global variables instead of function variables
    # t1 is thread 1 check if it is alive and only stop thread if thread is alive
    global t1, is_alive
    if is_alive:
        # Clear and update display
        clear_dir(['music'])
        clear_display(heading_text1, heading_text2, main_screen_text)
        display("App has Stopped,Press start", 1)
        display("Stopped", 2)
        display("Press start to start the program", 4)
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
@handle_error
def on_restart():
    """
        The function restarts thread when restart button is clicked.
    """
    on_stop()
    on_start()
    # Updated display
    display("Restarted", 1)


@handle_error
def clear_display(*args):
    """
        The function is used to clear display.
    """
    # *args accepts set of commands as ex: clear_display(1,2) if we print(args) -> (1,2)
    for elem in args:
        # for all elements inside args apply set method
        # Set is a method of tkinter set("") which sets display to null/clears display
        elem.set("")


# On clear screen
@handle_error
def on_clear():
    clear_display(heading_text1, main_screen_text)


# Displays text on screen according to choice.There are four displays in the app
# Ex:display("Hello", 1) displays "Hello" on first display
@handle_error
def display(value, choice):
    """
        The function is used to show display.
        Parameters:
            value (str): Text to display.
            choice (int): Screen number.
    """
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
@handle_error
def timeout(func, sec):
    root.after(sec, func)


# Tweak volume of pc
@handle_error
def tweak_volume(volume_points, volume_up=True):
    """
        The function is used to tweak volume.
        Parameters :
            volume_points (int): Volume points to tweak.
            volume_up (bool): Volume up or down according to true or false.
    """
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
@handle_error
def on_help():
    """
        The function is used to open help text.
    """
    path = os.getcwd()
    # path.join is used to join path because even if we forget to put / it adds itself
    path_of_file = os.path.join(path, 'help/help.txt')
    os.startfile(path_of_file, 'open')

@handle_error
def set_theme(theme_name,theme_id):
    """
        The function to change the theme.
    """
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
    global thememenu
    menubar.delete(4)
    cur_theme_submenu_bg={
        'initial':'white',
        'highlight':theme_name['app-disp-bg']
    }
    cur_theme_submenu_fg={
        'initial': 'black',
        'highlight': theme_name['main-txt']
    }
    cur_theme_colors=[0,1,2,3]
    theme_arr = [0]*4
    theme_arr[theme_id-1]=1
    thememenu = Menu(menubar, tearoff=0)
    bg_colors = list(map(lambda x, y: cur_theme_submenu_bg['highlight'] if bool(y) else cur_theme_submenu_bg['initial'],
                         cur_theme_colors,theme_arr))
    fg_colors = list(map(lambda x, y: cur_theme_submenu_fg['highlight'] if bool(y) else cur_theme_submenu_fg['initial'],
                         cur_theme_colors,theme_arr))
    thememenu.add_command(label="Light theme",background=bg_colors[0],foreground=fg_colors[0],command=lambda: set_theme(theme['white_theme'],1))
    thememenu.add_command(label="Dark theme",background=bg_colors[1],foreground=fg_colors[1], command=lambda: set_theme(theme['black_theme'],2))
    thememenu.add_command(label="Warm theme",background=bg_colors[2],foreground=fg_colors[2], command=lambda: set_theme(theme['orange_theme'],3))
    thememenu.add_command(label="Cool theme",background=bg_colors[3],foreground=fg_colors[3], command=lambda: set_theme(theme['blue_theme'],4))
    menubar.add_cascade(label="Theme", menu=thememenu)
    # Cache data every time user changes theme
    @handle_error
    def write_to_cache(filename, filedata):
        dt.write_jsonfile(filename, filedata)
    # Call the function
    write_to_cache('cache_theme.json', [theme_name, theme_id])

@handle_error
def on_submit():
    """
        The function is used to submit.
    """
    global inputValue
    inputValue = textBox.get("1.0", "end-1c")
    print(inputValue)
    # Remove blocking of code on submit button click
    block.set(False)
    textBox.delete("1.0", 'end')
    print("done waiting.")


if __name__ == '__main__':
    # Set default theme of the app
    # Retrieve cached data from cache_theme file if present
    @handle_error
    def retrieve_cached_theme(file_name):
        if (dt.read_jsonfile(file_name)): return dt.read_jsonfile(file_name)
    # Place the returned value in a variable named res
    res= retrieve_cached_theme('cache_theme.json')
    # Check if returned result is not empty, if it is not empty then destructure result
    if res:[cur_theme, theme_id]=res
    # If resposne is empty (usually when an error occurs or if file is not present) return default theme (hard coded)
    else:[cur_theme, theme_id]=[theme['black_theme'], 2]
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
                          pady=10,)
    # Set main screen text upon start of app
    main_screen_text.set(out_txt)
    textBox = Text(root, height=1, width=20)
    textBox.pack()
    submit_btn = Button(root, borderwidth=0, fg=cur_theme['btn']['start-fg'], activebackground='#025aa5',
                        activeforeground='white',
                        bg=cur_theme['btn']['start-bg'], text="Submit", command=lambda: on_submit(),
                        font=('Lucida Sans Typewriter', 8))
    # button = tk.Button(root, text="Click Me", command=lambda: var.set(1))
    # button.place(relx=.5, rely=.5, anchor="c")
    submit_btn.pack()

    # Show default display upon app start
    display("Stopped", 2)
    display("Stopped , Press Start", 1)
    # Start button creation and design and bg and fg are set to variable so that they can be controlled by set_theme function
    start_btn_txt = tk.StringVar()
    # Creating a photoimage object to use image
    startphoto = PhotoImage(file=r"./images/start.png")
    start_image = startphoto.subsample(1, 1)
    start_btn = Button(root, borderwidth=0, fg=cur_theme['btn']['start-fg'], activebackground='#025aa5',
                       activeforeground='white',
                       bg=cur_theme['btn']['start-bg'], image = start_image,text="Start",compound = RIGHT, command=on_start,
                       font=('Helvetica', 12, 'bold'), padx=6, pady=6)
    start_btn_txt.set('Start')
    start_btn.pack(side=LEFT)
    # Stop button creation and design and bg and fg are set to variable so that they can be controlled by set_theme function
    stop_btn_txt = tk.StringVar()
    stopphoto = PhotoImage(file=r"./images/stop.png")
    stop_image = stopphoto.subsample(1, 1)
    stop_btn = Button(root, borderwidth=0, fg=cur_theme['btn']['stop-fg'], activebackground='#ed0202',
                      activeforeground='white', bg=cur_theme['btn']['stop-bg'],
                      textvariable=stop_btn_txt, command=on_stop, font=('Helvetica', 12, 'bold'), padx=6, pady=6,image=stop_image,compound=RIGHT)
    stop_btn_txt.set('Stop')
    stop_btn.pack(side=LEFT, padx=60, pady=10)
    # Restart button creation and design and bg and fg are set to variable so that they can be controlled by set_theme function
    restart_btn_txt = tk.StringVar()
    restartphoto = PhotoImage(file=r"./images/rest.png")
    restart_image = restartphoto.subsample(12,12)
    restart_btn = Button(root,borderwidth=0, fg=cur_theme['btn']['rstart-fg'], activebackground='#40556a',
                         activeforeground='white', bg=cur_theme['btn']['rstart-bg'],
                         textvariable=restart_btn_txt, command=on_restart, font=('Helvetica', 12, 'bold'), padx=6,
                         pady=6,image=restart_image,compound=RIGHT)
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
    # Call change theme function to set current theme for first time
    # We are using destructured variable as arguments
    set_theme(cur_theme,theme_id)
    # Put default settings to main window
    root.configure(background=cur_theme['app-bg'], pady=10, padx=10, menu=menubar)
    # Start app now.
    root.mainloop()
