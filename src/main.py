#!/usr/bin/env python3

import time
import random

import graphics

from math import *


WINDOW_WIDTH = 850
WINDOW_HEIGHT = 550

INITIAL_FOOD = 100
FOOD_MIN_RADIUS = 4
FOOD_MAX_RADIUS = 5

INITIAL_PLAYER_WEIGHT = 10
PLAYER_MIN_MOVEMENT = 20.0
PLAYER_MIN_WEIGHT = 8
PLAYER_SMALLIZE_SPEED = 0.1


_current_id = 0
def generate_id():
    global _current_id

    return _current_id


def length(vec):
    return sqrt(vec.x * vec.x + vec.y * vec.y)


def normalize(vec):
    return vec * (1.0 / length(vec))


# Let S denote to weight
#  r  = 3 * sqrt(S * 2)
# |v| = max{115 - S / 4, 1}
class Player(graphics.Drawable):
    """Player is a big circle"""
    def __init__(self, position = None, color = None, id = None):
        super(Player, self).__init__()

        if position is None:
            position = graphics.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        if color is None:
            color = graphics.random_color()
        if id is None:
            self._id = generate_id()

        self._mergable = False
        self._weight = 0
        self._instance = graphics.CircleShape()
        self.weight = INITIAL_PLAYER_WEIGHT
        self._instance.point_count = 128
        self._instance.fill_color = color
        self.position = position

        self._direction = graphics.Vector2(0, 0)
        self._direction_point = self.position
        self._last_time = time.time()
    
    @property
    def position(self):
        return self._instance.position + (self._instance.radius, self._instance.radius)

    @position.setter
    def position(self, value):
        self._instance.position = value - (self._instance.radius, self._instance.radius)

        if self.position.x < 0:
            self.position = graphics.Vector2(0, self.position.y)
        elif self.position.x > WINDOW_WIDTH:
            self.position = graphics.Vector2(WINDOW_WIDTH, self.position.y)

        if self.position.y < 0:
            self.position = graphics.Vector2(self.position.x, 0)
        elif self.position.y > WINDOW_HEIGHT:
            self.position = graphics.Vector2(self.position.x, WINDOW_HEIGHT)


    @property
    def radius(self):
        return self._instance.radius

    @radius.setter
    def radius(self, value):
        pos = self.position
        self._instance.radius = value
        self.position = pos

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        if value < PLAYER_MIN_WEIGHT:
            return

        self._weight = value
        self.radius = 4 * sqrt(value)

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = normalize(value - self.position)
        self._direction_point = value

    def _update_movement(self, delta):
        speed = max(120 - 2 * sqrt(self.weight), PLAYER_MIN_MOVEMENT)
        offest = self.direction * speed * delta

        if length(self.position - self._direction_point) > 1:
            self.position += offest

    def _update_weight(self, delta):
        self.weight -= PLAYER_SMALLIZE_SPEED * delta

    def update(self):
        delta_time = time.time() - self._last_time
        self._last_time = time.time()

        self._update_movement(delta_time)
        self._update_weight(delta_time)

    def draw(self, target, states):
        target.draw(self._instance, states)


foods = []
player = Player()


def produce_food(position):
    radius = random.randint(FOOD_MIN_RADIUS, FOOD_MAX_RADIUS);

    circle = graphics.CircleShape()
    circle.point_count = 16
    circle.radius = radius;
    circle.fill_color = graphics.random_color()
    circle.position = position - (radius, radius);

    return circle


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


def update():
    global foods
    global player

    for i in range(0, len(foods)):
        if length(
                foods[i].position - player.position + (foods[i].radius, foods[i].radius)
            ) <= player.radius:
            player.weight += 1
            foods[i] = random_food()

    player.direction = graphics.Mouse.get_position(graphics.window)
    player.update()


def render():
    graphics.clear()

    for food in foods:
        graphics.draw(food)

    graphics.draw(player)

    graphics.present()


# Entrance

graphics.create_window()

graphics.set_handler(graphics.CloseEvent, lambda sender, args : close_window())
graphics.set_handler(graphics.MouseButtonEvent, on_mouse_click)

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
