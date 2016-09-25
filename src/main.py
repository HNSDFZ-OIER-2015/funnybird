#!/usr/bin/env python3

import time
import random

import utility
import graphics

from math import *

from ball import Ball


WINDOW_WIDTH = 850
WINDOW_HEIGHT = 550

INITIAL_FOOD = 100
FOOD_MIN_RADIUS = 4
FOOD_MAX_RADIUS = 5


foods = []
animation = []
player = Ball()


def produce_food(position):
    food = Ball()
    food.weight = 1
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

    if args.pressed:
        if args.code == graphics.Keyboard.W:
            if player.weight > 20 and not shotted:
                shotted = True
                animation.append(player.split(1))
        elif args.code == graphics.Keyboard.SPACE:
            if player.weight > 30:
                animation.append(player.split(int(player.weight / 2)))
    elif args.released:
        shotted = False


def update():
    global foods
    global player

    for i in range(0, len(foods)):
        if utility.length(
                foods[i].position - player.position + (foods[i].radius, foods[i].radius)
            ) <= player.radius:
            player.weight += 1
            foods[i] = random_food()

    player.direction = graphics.Mouse.get_position(graphics.window)
    player.update()

    for splition in animation:
        splition.update()


def render():
    graphics.clear()

    for food in foods:
        graphics.draw(food)

    graphics.draw(player)

    for splition in animation:
        graphics.draw(splition)

    graphics.present()


# Entrance

graphics.create_window()

graphics.set_handler(graphics.CloseEvent, lambda sender, args : close_window())
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
