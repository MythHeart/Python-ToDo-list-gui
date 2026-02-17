#!/usr/bin/env python3

from kivy.app import App
from kivy.core.window import Window
from widgets import TEAL, MainWindow

Window.clearcolor = TEAL


class TodoApp(App):
    title = "Todo App"

    def build(self):
        return MainWindow()


if __name__ == "__main__":
    todoapp = TodoApp()
    todoapp.run()
