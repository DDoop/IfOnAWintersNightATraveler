import PySimpleGUI as sg

import Models
from aitextgen import aitextgen


class Generator:
    model = Models.current_model
    model_loaded = False

    def generate(self, prompt: str, length: int, n: int, temperature: float, ):
        self.prompt = prompt
        self.word_count = length
        self.n = n
        self.temperature = temperature

        self.window.perform_long_operation(lambda:
                                           self._ai.generate(prompt=prompt,
                                                             max_length=length,
                                                             temperature=temperature,
                                                             return_as_list=True,
                                                             n=n),
                                           "-TEXT_GENERATED-"
                                           )

    def get_model(self):
        if sg.user_settings_get_entry("cache_dir") is not None:
            self._ai = aitextgen(model=Models.current_model, cache_dir=sg.user_settings_get_entry("cache_dir"))
            self.model_loaded = True
        else:
            self._ai = aitextgen(model=Models.current_model)
            self.model_loaded = True

    def load_model(self):
        self.model_loaded = False
        self.window.perform_long_operation(lambda:
                                           self.get_model(),
                                           "-MODEL_LOADED-"
                                           )

    def __init__(self, window):
        self.window = window
        self._ai = None
        self.prompt = None
        self.word_count = None
        self.n = None
        self.temperature = None
        self.load_model()
