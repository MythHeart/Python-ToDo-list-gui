#!/usr/bin/env python3

from kivy.uix.floatlayout import FloatLayout
from kivy.effects.scroll import ScrollEffect
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

GREY = (61 / 255, 61 / 255, 61 / 255, 1.0)
YELLOW = (1.0, 0.85, 0, 1.0)
LIGHT_TEAL = (0, 0.41, 0.41, 1.0)


class MainWindow(FloatLayout):
    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        todo_list_container = BoxLayout(
            orientation="vertical",
            size_hint=[0.85, None],
            height=350,
            pos_hint={"center_x": 0.5, "top": 0.85},
            spacing=10,
        )
        title_label = Label(
            font_size=35,
            text="[b]ToDo App[/b]",
            size_hint=[1, None],
            markup=True,
        )
        self.add_widget(todo_list_container)
        self.inputframe = InputFrame(self)
        self.show_existing_items()

        todo_list_container.add_widget(title_label)
        todo_list_container.add_widget(self.inputframe)

    def add_todo_item(self, todo_item):
        if todo_item.isspace() or todo_item == "":
            return
        self.db.add_todo_item(todo_item)
        self.todoitems.clear_widgets()
        self.show_existing_items()
        self.inputframe.todo_input_widget.text = ""

    def delete_todo_item(self, item_id):
        for item in self.todoitems.children:
            if item.item_id == item_id:
                self.db.delete_todo_item(item_id)
                item.parent.remove_widget(item)

    def mark_as_done(self, item_id):
        for item in self.todoitems.children:
            if item.item_id == item_id:
                self.db.mark_as_done(item_id)
                item.mark_done_button.disabled = True

    def show_existing_items(self):
        items = self.db.retrieve_all_items()
        for item_data in reversed(items):
            item_id, todo_item, done = item_data
            item_widget = Item(self, item_id, todo_item, done)
            self.todoitems.add_widget(item_widget)


class Input(TextInput):
    max_length = 99
    multiline = False

    def insert_text(self, *args):
        if len(self.text) < self.max_length:
            super().insert_text(*args)


class NoBackgroundButton(Button):
    background_down = ""
    background_normal = ""
    background_disabled = ""


class YellowButton(NoBackgroundButton):
    background_color = YELLOW
    color = GREY


class LightTealButton(NoBackgroundButton):
    background_color = LIGHT_TEAL


class InputFrame(BoxLayout):
    spacing = 8
    height = 45
    size_hint_y = None

    def __init__(self, main_window, **kwargs):
        super().__init__(**kwargs)

        self.todo_input_widget = Input(hint_text="Enter an activity", font_size=22)
        self.todo_input_widget.padding = [10, 10, 10, 10]
        add_item_button = YellowButton(width=self.height, size_hint=[None, 1], text="+")
        add_item_button.bind(
            on_release=lambda *args: main_window.add_todo_item(
                self.todo_input_widget.text
            )
        )
        self.add_widget(self.todo_input_widget)
        self.add_widget(add_item_button)
