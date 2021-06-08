import speech_recognition as sr
import data as dt
from gtts import gTTS
import pyautogui
import functions
from functions import *
# from functions import handle_error
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
from tkinter import messagebox
import ctypes
import threading

try:
    from plyer import notification
except Exception as e:
    print(e)

# importing web driver from selenium
from selenium import webdriver

####################################################################################
# ----------------------------------- GUI DESIGN --------------------------------- #
####################################################################################
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
def change_theme(theme_name):
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
    # Set text variables of variables
    # so that they can be modified later to update display
    # global notify_heading_text,main_screen_text,heading_text1,notify_heading_text
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
                        bg=cur_theme['btn']['start-bg'], text="Submit", command=lambda: on_submit(),
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
