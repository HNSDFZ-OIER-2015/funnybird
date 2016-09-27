#!/usr/bin/env python3

import time
import random

import utility
import graphics

from math import *

from ball import Ball
from player import Player


WINDOW_WIDTH = 850
WINDOW_HEIGHT = 550

INITIAL_FOOD = 100

foods = []
player = Player()


def produce_food(position):
    food = Ball()
    food.weight = 10
    food.position = position

    return food


def random_food():
    return produce_food(graphics.Vector2(
        random.randrange(0, WINDOW_WIDTH),
        random.randrange(0, WINDOW_HEIGHT)
    ))


def add_food(position):
    global foods

    foods.append(produce_food(position))


def on_mouse_click(sender, args):
    if args.released:
        add_food(args.position)


shotted = False
def on_keypress(sender, args):
    global shotted
    global player
    global foods

    if args.pressed:
        if args.code == graphics.Keyboard.W:
            if not shotted:
                shotted = True
                player.balls += player.shot()
        elif args.code == graphics.Keyboard.SPACE:
            player.split()
    elif args.released:
        shotted = False


def update():
    global foods
    global player

    for i in range(0, len(foods)):
        if player.try_eat(foods[i]):
            foods[i] = random_food()

    player.set_direction(graphics.Mouse.get_position(graphics.window))
    player.update()


def render():
    graphics.clear()

    for food in foods:
        graphics.draw(food)

    graphics.draw(player)

    graphics.present()


# Entrance

graphics.create_window()

graphics.set_handler(graphics.CloseEvent, lambda sender, args : graphics.close_window())
graphics.set_handler(graphics.MouseButtonEvent, on_mouse_click)
graphics.set_handler(graphics.KeyEvent, on_keypress)

graphics.set_background(graphics.Color(31, 45, 53))

for i in range(0, INITIAL_FOOD):
    INITIAL_PLAYER_RADIUS = 7

    add_food(graphics.Vector2(
        random.randrange(0, WINDOW_WIDTH), random.randrange(0, WINDOW_HEIGHT)
    ))

while graphics.is_open():
    graphics.do_events()

    update()
    render()
