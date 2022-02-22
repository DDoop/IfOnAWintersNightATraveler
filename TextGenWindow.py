import os

import PySimpleGUI as sg

import Generator
import Layout


class TextGenWindow(sg.Window):
    def __init__(self):
        super().__init__("Text Generator", Layout.MainLayout.layout, finalize=True)
        self.result_window = None
        self.settings_window = None
        self.result_window_active = False
        self.settings_window_active = False

        if not os.path.isdir("aitextgen") and sg.user_settings_get_entry("cache_dir") is None:
            new_dir = sg.PopupGetFolder(
                title="Cache size warning",
                message="Would you like to change the folder the models are stored in?\n"
                        "By default they will be saved in a folder alongside the executable called 'aitextgen'.\n"
                        "Close or cancel for default behavior.\n"
                        "This window only appears if the 'aitextgen' folder is missing and there is no set alternative."
            )
            if new_dir is not None:
                sg.user_settings_set_entry("cache_dir", new_dir)

        self.generator = Generator.Generator(self)

    def new_result_set_from_result(self, new_prompt):
        self['-PROMPT-'].update(value=new_prompt)

        self['-GENERATE-'].click()
        pass
