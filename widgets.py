#!/usr/bin/env python3

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


class NoBackgroundButton(Button):
    background_down = ""
    background_normal = ""
    background_disabled = ""


class YellowButton(NoBackgroundButton):
    background_color = YELLOW
    color = GREY


class LightTealButton(NoBackgroundButton):
    background_color = LIGHT_TEAL


class Input(TextInput):
    pass


class InputFrame(BoxLayout):
    spacing = 8
    height = 45
    size_hint_y = None

    def __init__(self, main_window, **kwargs):
        super().__init__(**kwargs)

        self.main_window = main_window

        self.todo_input_widget = Input(hint_text="Enter a todo activity", font_size=22)

        self.todo_input_widget.padding = [10, 10, 10, 10]

        add_button = YellowButton(text="+", width=self.height, size_hint=(None, 1))

        add_button.bind(
            on_release=lambda *args: main_window.add_todo_item(
                self.todo_input_widget.text
            )
        )

        self.add_widget(self.todo_input_widget)
        self.add_widget(add_button)


class ScrollableList(ScrollView):
    effect_cls = ScrollEffect

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.height = 400

        self.container = BoxLayout(orientation="vertical", spacing=5, size_hint_y=None)

        self.container.bind(minimum_height=self.container.setter("height"))

        self.add_widget(self.container)


class Item(BoxLayout):
    size_hint = (1, None)
    spacing = 5

    def __init__(self, main_window, item_id, todo_item, done=False, **kwargs):
        super().__init__(**kwargs)

        self.item_id = item_id
        self.height = 40

        description = LightTealButton(text=todo_item, size_hint=(0.6, 1))

        self.mark_done_button = YellowButton(
            text="Done", size_hint=(None, 1), width=100, disabled=done
        )

        self.mark_done_button.bind(
            on_release=lambda *args: main_window.mark_as_done(item_id)
        )

        remove_button = YellowButton(text="-", size_hint=(None, 1), width=40)

        remove_button.bind(
            on_release=lambda *args: main_window.delete_todo_item(item_id)
        )

        self.add_widget(description)
        self.add_widget(self.mark_done_button)
        self.add_widget(remove_button)


class MainWindow(FloatLayout):
    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)

        self.db = db

        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        title = Label(text="Todo App", font_size=32, size_hint_y=None, height=50)

        self.inputframe = InputFrame(self)

        self.todo_list = ScrollableList()

        layout.add_widget(title)
        layout.add_widget(self.inputframe)
        layout.add_widget(self.todo_list)

        self.add_widget(layout)

        self.show_existing_items()

    def add_todo_item(self, todo_item):
        if todo_item.strip():
            item_id = self.db.add_item(todo_item)

            self.todo_list.container.add_widget(Item(self, item_id, todo_item))

            self.inputframe.todo_input_widget.text = ""

    def show_existing_items(self):

        for item in self.db.get_items():
            item_id = item[0]
            text = item[1]
            done = item[2]

            self.todo_list.container.add_widget(Item(self, item_id, text, done))

    def delete_todo_item(self, item_id):

        self.db.delete_item(item_id)

        for widget in self.todo_list.container.children:
            if widget.item_id == item_id:
                self.todo_list.container.remove_widget(widget)
                break

    def mark_as_done(self, item_id):

        self.db.mark_as_done(item_id)

        for widget in self.todo_list.container.children:
            if widget.item_id == item_id:
                widget.mark_done_button.disabled = True
                break
