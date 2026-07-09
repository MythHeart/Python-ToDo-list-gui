#!/usr/bin/env python3

from kivy.app import App
from kivy.core.window import Window
from widgets import GREY, MainWindow
from database import Database

Window.clearcolor = GREY


class TodoApp(App):
    title = "Todo App"

    def build(self):
        self.db = Database()
        return MainWindow(db=self.db)

    def on_stop(self):
        if hasattr(self, "db"):
            try:
                self.db.close()
            except Exception:
                pass


if __name__ == "__main__":
    todoapp = TodoApp()
    todoapp.run()
