from textwrap import wrap

import PySimpleGUI as sg

import Models


def place(elem):
    """
    Places element provided into a Column element so that its placement in the layout is retained.
    :param elem: the element to put into the layout
    :return: A column element containing the provided element
    """
    return sg.Column([[elem]], pad=(0, 0))


sg.theme('DarkAmber')


class MainLayout:
    layout = [
        [
            sg.Menu([
                ["File", ["Settings", "Exit"]]
            ])
        ],
        [
            sg.Text('Currently loaded model:'),
            sg.Text("Model pending...", key="-MODEL_LABEL-"),
            sg.Text("", key="-MODEL_LOCATION-"),
        ],
        [
            sg.Listbox(
                Models.models, enable_events=True, key="-MODEL_SELECT-", disabled=True, size=(25, 5),
                select_mode="LISTBOX_SELECT_MODE_SINGLE"
            ),
            sg.Btn("Swap models", key="-MODEL_SWAP-", disabled=True)
        ],
        [
            sg.Text('Prompt string:')
        ],
        [
            sg.InputText("If on a winter's night a traveler", key="-PROMPT-"), sg.Text("Strings to generate"),
            sg.Spin([x for x in range(1, 21)], key='-SPIN-', size=(4, 1))
        ],
        [
            sg.Text("Temperature:"),
            sg.Input(key='-TEMPERATURE-', enable_events=True, default_text='1.0', size=(6, 1)),
        ],
        [
            sg.Text("Word length:"),
            sg.Slider((50, 750), key='-WORD_LENGTH-', enable_events=True, orientation="horizontal", expand_x=True)
        ],
        [
            sg.Button('Generate', key="-GENERATE-", disabled=True),
            sg.Check("Open result window", key="-RESULT_WINDOW_TOGGLE-", default=True),
            place(sg.Text("", visible=False, key="-RESULTS_ALERT-")),
            place(sg.Button('Halt', visible=False, key="-HALT-", tooltip="TODO")),
        ],
    ]


class ResultsLayout:
    @staticmethod
    def generate_results_layout(gen, results, fname):
        return [
            [ResultsLayout._header(gen.temperature, gen.word_count)],
            [ResultsLayout._generate_result_table(results)],
            [ResultsLayout._footer(fname)]
        ]

    @staticmethod
    def _header(temp, length):
        return [
                   sg.Text("Batch Info"),
                   sg.Text("Temperature:"),
                   sg.Text(temp, key="-RESULTS_TEMPERATURE-"),
                   sg.Text("Length:"),
                   sg.Text(length, key="-RESULTS_LENGTH-"),
               ],

    @staticmethod
    def _generate_result_table(results):
        result_table = []
        n = len(results)

        for i in range(n):
            result_table.extend(ResultsLayout._prepare_result_row(i, n, results[i]))

        return sg.Frame("Results",
                        [[sg.Column(
                            layout=result_table,
                            element_justification='left',
                            scrollable=True,
                            vertical_scroll_only=True,
                            expand_y=True,
                            expand_x=True,
                            key="-RESULTS_COLUMN-"
                        )]],
                        key="-RESULTS_FRAME-",
                        size=(511, 600),
                        expand_x=True,
                        expand_y=True,
                        )

    @staticmethod
    def calculate_row_height(text):
        y_size = 1
        if "\n" in text:
            y_size += text.count("\n")
        return y_size

    @staticmethod
    def _prepare_result_row(n, m, result):
        result = "\n".join(wrap(result, 60))
        y_size = ResultsLayout.calculate_row_height(result)

        rr = [
            [
                sg.Text(f"{n + 1} of {m}", key=f'-RESULT_{n}_POSITION-'),
            ],
            [
                sg.Text(f"{result.strip()}", key=f'-RESULT_{n}_TEXT-', size=(45, y_size)),
                sg.Column(
                    layout=[
                        [sg.Button("Copy", key=f'-COPY_RESULT_{n}-')],
                        [sg.Button("Submit\nas prompt", key=f'-SUBMIT_RESULT_{n}-', size=(7, 2))]
                    ],
                    element_justification="center"
                )
            ],
            [
                sg.HorizontalSeparator()
            ],
        ]
        return rr

    @staticmethod
    def _footer(fname):
        f = [
            sg.Text("Results written to"),
            sg.Text(fname, key="-RESULTS_FILE_LOCATION-")
        ]

        return f


class SettingsLayout:
    @staticmethod
    def generate_settings_layout():
        return [
            [
                sg.Text("Model cache directory:"),
            ],
            [
                sg.Input(
                    key='-SETTINGS_CACHE_DIR_INPUT-',
                    readonly=True,
                    default_text=sg.user_settings_get_entry("cache_dir"),
                    expand_x=True,
                    text_color='black'
                ),
                sg.FolderBrowse("Select", target="-SETTINGS_CACHE_DIR_INPUT-")
            ],
            [
                sg.HorizontalSeparator()
            ],
            [
                sg.Text("Load model to GPU:"),
                sg.Checkbox("Yes", key='-SETTINGS_LOAD_TO_GPU-', default=sg.user_settings_get_entry("on_gpu"))
            ],
            [
                sg.HorizontalSeparator()
            ],
            [
                sg.Column(
                    [
                        [
                            sg.Button("Save settings", key='-SETTINGS_SAVE-'),
                        ],
                    ],
                    justification='right',
                )
            ],
        ]
