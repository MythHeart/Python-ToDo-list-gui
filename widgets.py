#!/usr/bin/env python3

from kivy.uix.floatlayout import FloatLayout
from kivy.effects.scroll import ScrollEffect
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

GREY = (61/255, 61/255, 61/255, 1.0)


class MainWindow(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
