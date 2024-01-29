#Imports
import pyautogui
import time
import psutil
import win32gui
import win32process
from pywinauto import Application
import keyboard

#Globals
program_name = "Spotify.exe"


#Functions
def get_spotify_window_title(pids):
    titles = []
    returnpid = 0
    def _enum_cb(hwnd, results):
        if win32gui.IsWindowVisible(hwnd):
            pid = win32process.GetWindowThreadProcessId(hwnd)[1]
            if pids is None or pid in pids:
                nonlocal returnpid
                returnpid = pid
    win32gui.EnumWindows(_enum_cb, titles)
    return returnpid


def isOpen():
    for process in psutil.process_iter():
        try:
            if process.name() == program_name:
                print(f"Spotify is Open")
                break

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
        return True
    else:
        print(f'Spotify is not open!')
        return False


def run():
    if isOpen():
        spotify_pids = []
        process_name = "Spotify.exe"
        
        for proc in psutil.process_iter():
            if process_name in proc.name():
                spotify_pids.append(proc.pid)
                
                
        app = Application().connect(process=get_spotify_window_title(spotify_pids))
        app.top_window().set_focus()
        pyautogui.hotkey('alt', 'shift', 'b', interval=0.25)
        
        window = app.top_window()
        
        window.minimize()
        
        
#Keybind
def on_f9_press(e):
    if e.event_type == keyboard.KEY_DOWN:
        run()

keyboard.on_press_key('F9', on_f9_press)

keyboard.wait('F22') 