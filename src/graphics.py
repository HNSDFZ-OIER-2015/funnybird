import random

from sfml.system import *
from sfml.window import *
from sfml.graphics import *


window = None
event_handlers = {}
background_color = Color.BLACK


def create_window(width = 850, height = 550, title = "Game Window"):
    global window

    window = RenderWindow(VideoMode(width, height), title)
    window.framerate_limit = 60


def close_window():
    global window

    window.close()


def is_open():
    global window

    return window.is_open


def set_handler(event, handler):
    global event_handlers

    event_handlers[event] = handler


def set_background(color):
    global background_color

    background_color = color


def do_events():
    global window
    global event_handlers

    for event in window.events:
        if type(event) in event_handlers:
            event_handlers[type(event)](window, event);


def clear():
    global window
    global background_color

    window.clear(background_color)


def draw(shape):
    global window

    window.draw(shape)


def present():
    global window

    window.display()


def random_color():
    return Color(
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )


if __name__ == "__main__":
    create_window()
    set_handler(CloseEvent, lambda sender, args : close_window())
    set_background(Color(31, 45, 53))

    while is_open():
        do_events()
        clear()
        present()
