#!/usr/bin/env python3

from kivy.uix.floatlayout import FloatLayout

TEAL = (0, 0.31, 0.31, 1.0)


class MainWindow(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
