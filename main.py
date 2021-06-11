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
from selenium import webdriver
def error_message(title, body, choice):
    error_dict = {
        1: tk.messagebox.showinfo,
        2: tk.messagebox.showwarning,
        3: tk.messagebox.showerror
    }
    error_func = error_dict.get(choice, " ")
    error_func(title, body)
icon = {
    "error": "images/err.ico",
    "message": "images/msg.ico",
    "tkinter-title-icon": "images/assistant.png",
}
sender_email_info = {
    'user_name': 'superfighterpr@gmail.com',
    'user_password': os.getenv('device_mail_id')
}
lang = {
    'display-text': 'en',
    'input-speech': 'kn',
    'output-speech': 'kn',
}
api_keys = {
    'news_api': os.getenv('newsapi_api_key'),
    'weather_api': os.getenv('weather_api_key'),
    'youtube_api': os.getenv('youtube_api_key')
}
b_w = dt.retrieve_json_files(['bw.json'])[0][0]
theme = dt.retrieve_json_files(['theme.json'])[0][0]
commands = dt.retrieve_json_files(['commands.json'])[0][0]
error_codes = dt.retrieve_json_files(['errorcodes.json'])[0][0]
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
@handle_error
def testifarrayinline(arr, line):
    # It takes array of string and string line,
    # for every string in array put the string to elem
    for elem in arr:
        # if elem in line:
        if re.search(fr'({elem}+\s)|({elem}$)', line):
            return True
    return False
@handle_error
def remove_special_charecters(string, regexp='[^A-Za-z0-9\s]+', replace_many_space_with_onespace=True):
    clean_string = re.sub(regexp, '', string)
    if replace_many_space_with_onespace: return ' '.join(clean_string.split())
    return clean_string
@handle_error
def return_searched_word(arr, line):
    for elem in arr:
        if re.search(fr'({elem}+\s)|({elem}$)', line):
            return elem
    return ''
@handle_error
def send_mail():
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
@handle_error
def takeuserinput(lang='kn', msg='Listening...'):
    with sr.Microphone() as source:
        r = sr.Recognizer()
        print(msg)
        display(msg, 2)
        # hear=True
        r.pause_threshold = 0.6
        audio = r.listen(source)
        try:
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
            return None
    return query
@handle_error
def open_website(url, new_tab=0):
    webbrowser.open_new(url)
@handle_error
def say(music):
    playsound(music)
@handle_error
def text_translator(text,dest='kn'):
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
@handle_error
def etks(text, id=1):
    dir = f"music//eng{id}.mp3"
    kan_txt = text_translator(text, 'kn')
    display(kan_txt, 4)
    print(kan_txt)
    obj = gTTS(text=kan_txt, slow=False, lang='kn')
    obj.save(dir)
    say(dir)
    os.remove(dir)
@handle_error
def newsretriever(number=10, api_key=api_keys['news_api'], country='in', category='&category=business', q='&q=tesla'):
    x = []
    counter = 0
    news_list = []
    url = f'https://newsapi.org/v2/top-headlines?country={country}&language=en&apiKey={api_key}'
    x = requests.get(url, timeout=5)
    x = json.loads(x.text)
    if len(x) != 0:
        for id, cray in enumerate(x['articles']):
            counter += 1
            if counter > int(number):
                break
            regexp = '.*\s-\s'
            pattern = re.compile(r'.*\s-\s')
            result = re.search(pattern, cray['title']).group()
            clean_result = remove_special_charecters(result)
            news_list.append(clean_result)
        return news_list
@handle_error
def wish_time(hour=datetime.datetime.now().strftime("%H")):
    hour = int(hour)
    if 5 < hour < 12:return "Good morning"
    elif 12 <= hour < 17:return "Good Midday"
    elif 17 <= hour < 19:return "Good Evening"
    else:return "Good Night"
@handle_error
def bwc(cmd):
    for bw in b_w:
        if bw in cmd:
            return bw
    return ""
@handle_error
def curtime():
    return datetime.datetime.now().strftime("%H : %M ")
@handle_error
def ggap(tim=0.5):
    time.sleep(tim)
@handle_error
def create_dir(dir_array):
    for dir in dir_array:
        if not (path.exists(dir)):
            try:
                os.mkdir(dir)
            except Exception as e:
                print("Not able to make music directory inside [create_dir] :", e)
                error_message(f"Error e[{error_codes['dir-error']['dir']}]", 'Not able to make directory', 3)
@handle_error
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
@handle_error
def init():
    etks(wish_time())
    ggap()
    etks("I am kashvi,please tell me how may i help", 1)
@handle_error
def swm():
    etks("Speak the message you want to send when I start to listen")
    ggap()
    msg = takeuserinput('kn', 'Listening to message')
    etks("Enter the number to which you want to send a whatsapp message")
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
    pywhatkit.sendwhatmsg('+91' + num, msg, hr, mn)
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
        print("Notify error")
@handle_error
def utc_to_time(secsTillEpoch):
    local_time = time.ctime(secsTillEpoch)
    cur_time = datetime.datetime.strptime(local_time, '%a %b %d %H:%M:%S %Y')
    return cur_time
@run_async
@handle_error
def weather_report(latitude=13.66675, longitude=75.30914, api_key=api_keys['weather_api']):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid" \
          f"={api_key}&lang=en "
    json_object = {}
    w = {}
    json_object = json.loads(requests.get(url).text)
    w = json_object
    json_formatted_str = json.dumps(json_object, indent=2)
    if len(w) != 0:
        sunRiseSeconds = json_object['sys']['sunrise']
        sunSetSeconds = json_object['sys']['sunset']
        sunRiseTime = utc_to_time(sunRiseSeconds)
        sunSetTime = utc_to_time(sunSetSeconds)
        windInfo = f"  Wind is blowing at the speed of {w['wind']['speed']} and at direction of {w['wind']['deg']} degree."
        weatherInfo = f"  Today's weather  is {w['weather'][0]['main']} and has weather condition {w['weather'][0]['description']}.Cloud percentage is {w['clouds']['all']}."
        temperatureInfo = f"  Temperature is {round(w['main']['temp'] - 273.1, 2)} degree Celsius .It is feeling like {round(w['main']['feels_like'] - 273.15, 2)} degree Celsius."
        pressureInfo = f"  Pressure is {w['main']['pressure'] * 100} Pascal."
        humidityInfo = f"  Humidity is {w['main']['humidity']}%."
        sunRiseInfo = f"Expected sunrise {str(sunRiseTime.hour)} hour and {str(sunRiseTime.minute)} minute"
        sunSetInfo = f"Expected sunset {str(sunSetTime.hour - 12)} hour and {str(sunSetTime.minute)} minute"
        return windInfo + weatherInfo + temperatureInfo + pressureInfo + humidityInfo + sunRiseInfo + sunSetInfo
@run_async
@handle_error
def wikipedia_search(query, sentences=2):
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
    etks(f"Are you sure want to {action} computer")
    if testifarrayinline(commands['positive-statements'], takeuserinput('kn')):
        etks(f"Now computer will {action}")
        os.system(command)
    else:
        etks(f"Computer will not {action} due to your action or inaction")
@handle_error
def google_search(user_input="who is Prime Minister of India"):
    if testifarrayinline(commands['meaning'], user_input):
        query = user_input.replace(return_searched_word(commands['meaning'], user_input), '')
        english_query = text_translator(query, 'en')
        apended_eng_query = 'meaning of the word ' + english_query
        result = requests.get(f"https://www.google.com/search?q={apended_eng_query}")
        html_text = result.text
        html_parsed = BeautifulSoup(html_text, 'html.parser')
        match = html_parsed.find_all("div", {"class": "BNeawe s3v9rd AP7Wnd"})[2]
        return match.text
    else:
        user_input = text_translator(user_input, dest='en')
        result = requests.get(f"https://www.google.com/search?q={user_input}")
        html_text = result.text
        html_parsed = BeautifulSoup(html_text, 'html.parser')
        match = html_parsed.find('div', class_='BNeawe')
        return match.text
@handle_error
def get_youtube_link(query):
    youtube = build('youtube', 'v3', developerKey=api_keys['youtube_api'])
    req = youtube.search().list(q=query, part='snippet', type='video')
    video_id = req.execute()['items'][0]['id']['videoId']
    youtube_link = f'https://www.youtube.com/watch?v={video_id}'
    return youtube_link
@handle_error
def open_google_maps(url):
    global driver
    driver = webdriver.Chrome('C:\Program Files (x86)\chromedriver.exe')
    driver.get(url)
    ggap(5)
    button = driver.find_element_by_class_name("searchbox-searchbutton")
    button.click()
    time.sleep(2)
    button.click()
@handle_error
def recursive_input(lang='kn'):
    user_input = takeuserinput()
    while user_input is None:
        user_input = takeuserinput()
    return user_input
def is_valid(key,user_input):
    return testifarrayinline(commands[key], user_input)
count = 0
@handle_error
def main(commands=commands):
    global count
    if count == 0:
        pass
    user_input = recursive_input('kn')
    if (user_input is not None) and (user_input != 'None'):
        bwc(user_input)
        if is_valid('time',user_input):
            etks(curtime())
        elif is_valid('news',user_input):
            print('How')
            for news in newsretriever(2):
                etks(news)
        elif is_valid('wikipedia',user_input):
            wikiQueryKan = user_input.replace(return_searched_word(commands['wikipedia'], user_input),'')
            wikiQueryEng = text_translator(wikiQueryKan, 'en')
            result = wikipedia_search(wikiQueryEng)
            if result:
                etks("According to wikipedia")
                etks(result)
            else:
                etks("Sorry there is no information")
        elif is_valid('you-tube',user_input):
            yt_query = user_input.replace(return_searched_word(commands['you-tube'], user_input), '')
            open_website(get_youtube_link(text_translator(yt_query, 'kn')))
        elif is_valid('google',user_input):
            open_website("https://www.google.com")
        elif is_valid('twitter',user_input):
            open_website("https://twitter.com")
        elif is_valid('facebook',user_input):
            open_website("https://www.facebook.com")
        elif is_valid('instagram',user_input):
            open_website("https://www.instagram.com/")
        elif is_valid('weather',user_input):
            result = weather_report()
            if result:
                etks(result)
            else:
                error_message(f"Error e[{error_codes['unknown-error']['weather-report']}]", e, 3)
        elif is_valid('whatsapp',user_input):
            try:
                swm()
            except Exception as e:
                print("Inside main in whatsapp", e)
        elif is_valid('e-mail',user_input):
            send_mail()
        elif is_valid('power-off',user_input):
            tweak_power("shutdown /s /t 1", 'power-off')
        elif is_valid('restart',user_input):
            tweak_power("shutdown /r /t 1", 'restart')
        elif is_valid('sleep',user_input):
            tweak_power("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", 'sleep')
        elif is_valid('google-text',user_input):
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
        elif is_valid('map',user_input):
            map_query = user_input.replace(return_searched_word(commands['map'], user_input), '')
            open_google_maps(f"https://www.google.com/maps/place/{map_query}")
        else:
            pass
    main()
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
@handle_error
def on_start():
    clear_dir(['music'])
    global t1, is_alive
    if not is_alive:
        create_dir(['music', 'images', 'help', 'data'])
        display("Started", 1)
        clear_display(heading_text1, heading_text2, main_screen_text)
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
    else:
        error_message("Warning", "App is already started", 2)
@handle_error
def on_stop():
    global t1, is_alive
    if is_alive:
        clear_dir(['music'])
        clear_display(heading_text1, heading_text2, main_screen_text)
        display("App has Stopped,Press start", 1)
        display("Stopped", 2)
        display("Press start to start the program", 4)
        if t1 is not None:
            is_alive = False
            t1.raise_exception()
            t1 = None
    else:
        error_message("Warning", "App is already stopped", 2)
@handle_error
def on_restart():
    on_stop()
    on_start()
    display("Restarted", 1)
@handle_error
def clear_display(*args):
    for elem in args:
        elem.set("")
@handle_error
def on_clear():
    clear_display(heading_text1, main_screen_text)
@handle_error
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
@handle_error
def timeout(func, sec):
    root.after(sec, func)
@handle_error
def tweak_volume(volume_points, volume_up=True):
    if volume_up:
        for _ in range(volume_points):
            pyautogui.press("volumeup")
    else:
        for _ in range(volume_points):
            pyautogui.press("volumedown")
@handle_error
def on_help():
    path = os.getcwd()
    path_of_file = os.path.join(path, 'help/help.txt')
    os.startfile(path_of_file, 'open')
@handle_error
def set_theme(theme_name,theme_id):
    notification1.configure(bg=theme_name['app-bg'], fg=theme_name['n1-txt'])
    heading1.configure(bg=theme_name['app-disp-bg'], fg=theme_name['h1-txt'])
    heading2.configure(bg=theme_name['app-disp-bg'], fg=theme_name['h2-txt'])
    main_screen.configure(bg=theme_name['app-disp-bg'], fg=theme_name['main-txt'])
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
    @handle_error
    def write_to_cache(filename, filedata):
        dt.write_jsonfile(filename, filedata)
    write_to_cache('cache_theme.json', [theme_name, theme_id])
@handle_error
def on_submit():
    global inputValue
    inputValue = textBox.get("1.0", "end-1c")
    print(inputValue)
    block.set(False)
    textBox.delete("1.0", 'end')
    print("done waiting.")
if __name__ == '__main__':
    @handle_error
    def retrieve_cached_theme(file_name):
        if (dt.read_jsonfile(file_name)): return dt.read_jsonfile(file_name)
    res= retrieve_cached_theme('cache_theme.json')
    if res:[cur_theme, theme_id]=res
    else:[cur_theme, theme_id]=[theme['black_theme'], 2]
    t1 = None
    is_alive = False
    root = Tk()
    block = BooleanVar(root, False)
    root.title(os.getcwd() + '\\' + Path(__file__).name)
    root.iconphoto(True, tk.PhotoImage(file=icon["tkinter-title-icon"]))
    windowWidth = root.winfo_reqwidth()
    windowWidth = 400
    windowHeight = root.winfo_reqheight()
    windowHeight = 600
    print("Width", windowWidth, "Height", windowHeight)
    idth = root.winfo_reqwidth()
    positionRight = int(root.winfo_screenwidth() / 2 - windowWidth / 2)
    positionDown = int(root.winfo_screenheight() / 2 - windowHeight / 2)
    root.geometry("400x600+{}+{}".format(positionRight, positionDown))
    root.minsize(400, 600)
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
                          pady=10,)
    main_screen_text.set(out_txt)
    textBox = Text(root, height=1, width=20)
    textBox.pack()
    submit_btn = Button(root, borderwidth=0, fg=cur_theme['btn']['start-fg'], activebackground='#025aa5',
                        activeforeground='white',
                        bg=cur_theme['btn']['start-bg'], text="Submit", command=lambda: on_submit(),
                        font=('Lucida Sans Typewriter', 8))
    submit_btn.pack()
    display("Stopped", 2)
    display("Stopped , Press Start", 1)
    start_btn_txt = tk.StringVar()
    startphoto = PhotoImage(file=r"./images/start.png")
    start_image = startphoto.subsample(1, 1)
    start_btn = Button(root, borderwidth=0, fg=cur_theme['btn']['start-fg'], activebackground='#025aa5',
                       activeforeground='white',
                       bg=cur_theme['btn']['start-bg'], image = start_image,text="Start",compound = RIGHT, command=on_start,
                       font=('Helvetica', 12, 'bold'), padx=6, pady=6)
    start_btn_txt.set('Start')
    start_btn.pack(side=LEFT)
    stop_btn_txt = tk.StringVar()
    stopphoto = PhotoImage(file=r"./images/stop.png")
    stop_image = stopphoto.subsample(1, 1)
    stop_btn = Button(root, borderwidth=0, fg=cur_theme['btn']['stop-fg'], activebackground='#ed0202',
                      activeforeground='white', bg=cur_theme['btn']['stop-bg'],
                      textvariable=stop_btn_txt, command=on_stop, font=('Helvetica', 12, 'bold'), padx=6, pady=6,image=stop_image,compound=RIGHT)
    stop_btn_txt.set('Stop')
    stop_btn.pack(side=LEFT, padx=60, pady=10)
    restart_btn_txt = tk.StringVar()
    restartphoto = PhotoImage(file=r"./images/rest.png")
    restart_image = restartphoto.subsample(12,12)
    restart_btn = Button(root,borderwidth=0, fg=cur_theme['btn']['rstart-fg'], activebackground='#40556a',
                         activeforeground='white', bg=cur_theme['btn']['rstart-bg'],
                         textvariable=restart_btn_txt, command=on_restart, font=('Helvetica', 12, 'bold'), padx=6,
                         pady=6,image=restart_image,compound=RIGHT)
    restart_btn_txt.set('Restart')
    restart_btn.pack(side=RIGHT)
    menubar = Menu(root, relief=FLAT, bd=0)
    appmenu = Menu(menubar, tearoff=0)
    appmenu.add_command(label="Start", command=on_start)
    appmenu.add_command(label="Stop", command=on_stop)
    appmenu.add_command(label="Restart", command=on_restart)
    appmenu.add_command(label="Clear", command=on_clear)
    appmenu.add_separator()
    appmenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="App", menu=appmenu)
    volumemenu = Menu(menubar, tearoff=0)
    volumemenu.add_command(label="Volume Up", command=lambda: tweak_volume(10, True))
    volumemenu.add_command(label="Volume Down", command=lambda: tweak_volume(8, False))
    volumemenu.add_command(label="Mute/unmute", command=lambda: pyautogui.press("volumemute"))
    menubar.add_cascade(label="Volume", menu=volumemenu)
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Help to operate app", command=on_help)
    helpmenu.add_command(label="About us", command=lambda: print("K"))
    menubar.add_cascade(label="Help", menu=helpmenu)
    set_theme(cur_theme,theme_id)
    root.configure(background=cur_theme['app-bg'], pady=10, padx=10, menu=menubar)
    root.mainloop()
