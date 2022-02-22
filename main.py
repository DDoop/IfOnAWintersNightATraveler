import PySimpleGUI as sg

import EventLoop
import TextGenWindow

sg.user_settings_filename(path=".")
window = TextGenWindow.TextGenWindow()

while True:
    if EventLoop.MainEventLoop.main_event_loop(window) == -1:
        break

    if window.result_window_active:
        if EventLoop.ResultEventLoop.r_event_loop(window) == -1:
            window.result_window_active = False
            window.result_window = None

    if window.settings_window_active:
        if EventLoop.SettingsEventLoop.settings_event_loop(window) == -1:
            window.settings_window_active = False
            window.settings_window = None

window.close()
