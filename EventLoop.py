import datetime as dt
from tkinter import Tk

import PySimpleGUI as sg

import Layout
import Models
from TextGenWindow import TextGenWindow
from util import save_text_to_file


class MainEventLoop:
    @staticmethod
    def main_event_loop(window: TextGenWindow):
        event, values = window.read(timeout=100)

        generator = window.generator

        if event == sg.WIN_CLOSED or event == 'Exit' or event == '-EXIT-':
            if window.result_window:
                window.result_window.close()
            return -1

        MainEventLoop.text_generation_behavior(event, values, window, generator)
        MainEventLoop.model_swapping_behavior(event, values, window, generator)

        if event == '-IN-' and values['-IN-'] and values['-IN-'][-1] not in ('0123456789.-'):
            window['-IN-'].update(values['-IN-'][:-1])

        if event == "Settings":
            SettingsEventLoop.settings_popup(window)

        if event == "-HALT-":
            # TODO
            pass

    @staticmethod
    def text_generation_behavior(event, values, window, generator):
        if event == "-GENERATE-":
            window.set_cursor("watch")
            window['-GENERATE-'].update(disabled=True)
            window['-MODEL_SELECT-'].update(disabled=True)
            if not window['-HALT-'].visible:
                window['-HALT-'].update(visible=True)
            window['-HALT-'].update(disabled=False)

            temperature = float(values['-TEMPERATURE-'])
            prompt = values["-PROMPT-"]
            iter_count = values['-SPIN-']
            word_count = int(values["-WORD_LENGTH-"]) + len(prompt)

            generator.generate(prompt=prompt, length=word_count, n=iter_count, temperature=temperature)

            window['-RESULTS_ALERT-'].update(value=f"Results pending...")
            if not window['-RESULTS_ALERT-'].visible:
                window['-RESULTS_ALERT-'].update(visible=True)

        if event == "-TEXT_GENERATED-":
            window.set_cursor("")
            txt = f"Model: {Models.current_model}\nPrompt: {generator.prompt}\nTemperature: {generator.temperature}\n\
Length: {generator.word_count}\n"

            txt += "-" * 50 + '\n'
            for i in range(len(values['-TEXT_GENERATED-'])):
                txt += f'{i + 1} of {len(values["-TEXT_GENERATED-"])}' + '\n'
                txt += values['-TEXT_GENERATED-'][i] + '\n'
                txt += "-" * 50 + '\n'

            fname = f"results/{dt.datetime.now().strftime('%d.%m.%y, %H.%M')}.txt"
            save_text_to_file(fname, txt)
            window.ding()
            window['-RESULTS_ALERT-'].update(value=f"Results saved to:\n {fname}")
            if not window['-RESULTS_ALERT-'].visible:
                window['-RESULTS_ALERT-'].update(visible=True)
            window['-GENERATE-'].update(disabled=False)
            window['-HALT-'].update(disabled=True)
            window['-MODEL_SELECT-'].update(disabled=False)

            # LAUNCHES A WINDOW
            if values['-RESULT_WINDOW_TOGGLE-']:
                ResultEventLoop.results_popup(window, generator, values['-TEXT_GENERATED-'], fname)

    @staticmethod
    def model_swapping_behavior(event, values, window, generator):
        if event == "-MODEL_SELECT-":
            if values['-MODEL_SELECT-'][0] == Models.current_model:
                window['-MODEL_SWAP-'].update(disabled=True)
            elif generator.model_loaded and window['-MODEL_SWAP-'].Disabled:
                window['-MODEL_SWAP-'].update(disabled=False)

        if event == "-MODEL_LOADED-":
            window.ding()
            window.set_cursor("")

            window['-MODEL_SELECT-'].update(disabled=False)
            window['-MODEL_SWAP-'].update(disabled=False)
            window['-GENERATE-'].update(disabled=False)
            window.set_cursor('')
            window["-MODEL_LABEL-"].update(Models.current_model)

            # set the '-MODEL_SELECT-' to not equal the current model
            new_possible_model_index = Models.models.index(Models.current_model) + 1
            if new_possible_model_index > len(Models.models) - 1:
                new_possible_model_index = 0
            window['-MODEL_SELECT-'].update(set_to_index=new_possible_model_index)

        if event == "-MODEL_SWAP-":
            window.set_cursor("watch")
            window['-MODEL_SWAP-'].update(disabled=True)
            window['-MODEL_SELECT-'].update(disabled=True)
            window['-GENERATE-'].update(disabled=True)
            if not window['-HALT-'].visible:
                window['-HALT-'].update(visible=True)
            window['-HALT-'].update(disabled=False)

            window.set_cursor('wait')
            Models.current_model = values["-MODEL_SELECT-"][0]
            generator.load_model()
            window["-MODEL_LABEL-"].update("Model swap pending...")
        pass


class ResultEventLoop:
    @staticmethod
    def r_event_loop(main_window):
        r_window = main_window.result_window
        event, values = r_window.read(timeout=100)

        if event == sg.WIN_CLOSED or event == 'Exit' or event == '-EXIT-':
            r_window.close()
            return -1

        if event[:len('-COPY_RESULT')] == '-COPY_RESULT':
            n = int(event[len('-COPY_RESULT') + 1:-1])
            copy2clip(r_window[f'-RESULT_{n}_TEXT-'].DisplayText)
            return

        if event[:len('-SUBMIT_RESULT')] == '-SUBMIT_RESULT':
            n = int(event[len('-SUBMIT_RESULT') + 1:-1])
            new_prompt = r_window[f'-RESULT_{n}_TEXT-'].DisplayText
            main_window.new_result_set_from_result(new_prompt)
            return

    @staticmethod
    def results_popup(window, gen, results, fname):
        window.result_window_active = True
        l = Layout.ResultsLayout.generate_results_layout(gen, results, fname)
        if window.result_window:
            window.result_window.close()
        window.result_window = sg.Window("Results", layout=l, resizable=True, finalize=True)


class SettingsEventLoop:
    @staticmethod
    def settings_event_loop(main_window):
        s_window = main_window.settings_window
        event, values = s_window.read(timeout=100)

        if event == sg.WIN_CLOSED or event == 'Exit' or event == '-EXIT-':
            s_window.close()
            return -1

        if event == '-SETTINGS_SAVE-':
            yn = sg.PopupYesNo("This will close the application, is that ok?")
            if yn == 'Yes':
                sg.user_settings_set_entry("cache_dir", values['-SETTINGS_CACHE_DIR_INPUT-'])
                s_window.close()
                main_window.close()
                return -1
            if yn == "No":
                return

    @staticmethod
    def settings_popup(window):
        window.settings_window_active = True
        l = Layout.SettingsLayout.generate_settings_layout()
        if window.settings_window:
            window.settings_window.close()
        window.settings_window = sg.Window("Settings", layout=l, finalize=True)


def copy2clip(txt):
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(txt)
    r.update()  # now it stays on the clipboard after the window is closed
    r.destroy()
