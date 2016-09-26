import time
import random

import utility
import graphics

from math import *


INITIAL_BALL_WEIGHT = 10

BALL_MIN_MOVEMENT = 20.0
BALL_MIN_WEIGHT = 1
BALL_MIN_RADIUS = 4
BALL_SMALLIZE_SPEED = 0.1

BORDER_LEFT = 0
BORDER_RIGHT = 850
BORDER_TOP = 0
BORDER_BOTTOM = 550

BALL_MERGE_SPAN = 999


# Let S denote to weight
#  r  = 3 * sqrt(S * 2)
# |v| = max{115 - S / 4, 1}
class Ball(graphics.Drawable):
    """Ball is a big circle"""
    def __init__(self, position = None, color = None, id = None):
        super(Ball, self).__init__()

        if position is None:
            position = graphics.Vector2(
             (BORDER_RIGHT - BORDER_LEFT) / 2,
             (BORDER_BOTTOM - BORDER_TOP) / 2
         )
        if color is None:
            color = graphics.random_color()
        if id is None:
            id = utility.generate_id()

        self._id = id
        self._last_merge = time.time()
        self._mergable = False
        self._smooth_weight = 0
        self._forces = []
        self.temporary_forces = []

        self._weight = 0
        self._instance = graphics.CircleShape()
        self._instance.point_count = 128
        self.weight = INITIAL_BALL_WEIGHT
        self.color = color
        self.position = position

        self._direction = graphics.Vector2(0, 0)
        self._direction_point = self.position
        self._last_time = time.time()
    
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self):
        self._id = id

    @property
    def mergable(self):
        return self._mergable

    @mergable.setter
    def mergable(self, value):
        if value == False:
            self._last_merge = time.time()

        self._mergable = value

    @property
    def color(self):
        return self._instance.fill_color

    @color.setter
    def color(self, value):
        self._instance.fill_color = value

    @property
    def position(self):
        return self._instance.position + (self._instance.radius, self._instance.radius)

    @position.setter
    def position(self, value):
        if value.x < BORDER_LEFT:
            value.x = BORDER_LEFT
        elif value.x > BORDER_RIGHT:
            value.x = BORDER_RIGHT

        if value.y < BORDER_TOP:
            value.y = BORDER_TOP
        elif value.y > BORDER_BOTTOM:
            value.y = BORDER_BOTTOM
        
        self._instance.position = value - (self.radius, self.radius)

    @property
    def radius(self):
        return self._instance.radius

    @radius.setter
    def radius(self, value):
        if value < BALL_MIN_RADIUS:
            value = BALL_MIN_RADIUS

        pos = self.position
        self._instance.radius = value
        self.position = pos

        if value < 5:
            self._instance.point_count = 8
        elif value < 20:
            self._instance.point_count = 16
        elif value < 100:
            self._instance.point_count = 32
        elif value < 300:
            self._instance.point_count = 64
        else:
            self._instance.point_count = 128

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        if value < BALL_MIN_WEIGHT:
            return

        self._weight = value
        self.radius = 3 * sqrt(value)

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = utility.normalize(value - self.position)
        self._direction_point = value

    @property
    def speed(self):
        return Ball.speed_by_weight(self.weight)

    @property
    def forces(self):
        return self._forces

    @forces.setter
    def forces(self, value):
        self._forces = value

    def speed_by_weight(weight):
        return max(120 - 3 * sqrt(weight), BALL_MIN_MOVEMENT)

    @property
    def smooth_weight(self):
        return self._smooth_weight

    @smooth_weight.setter
    def smooth_weight(self, value):
        self._smooth_weight = value

    def split(self, value):
        if value < 1:
            raise ValueError("value should be greater than 1.")
        if value > self.weight:
            raise ValueError("value should be smaller than the weight of itself.")

        self.smooth_weight -= value
        new = Ball(
            position = self.position,
            color = self.color,
            id = self.id
        )
        new.direction = self.position + self._direction * (
            self.radius + Ball.speed_by_weight(value) * 0.7
        )
        new.weight = value
        new.forces.append([new.direction * 2, 1])

        return new

    def _update_movement(self, delta):
        dist = utility.length(self.position - self._direction_point)

        if dist < 1:
            return

        forcesum = graphics.Vector2(0, 0)
        for force in self._forces:
            forcesum += force[0]
        for force in self.temporary_forces:
            forcesum += force

        rate = min((dist / self.radius), 1)
        if len(self.temporary_forces) == 0:
            forcesum += self.direction
        offest = forcesum * self.speed * delta * rate
        self.position += offest
        self.temporary_forces.clear()

    def _update_weight(self, delta):
        smooth_delta = 0
        if abs(self.smooth_weight) < 2:
            smooth_delta = self.smooth_weight
            self.smooth_weight = 0
        else:
            smooth_delta = self.smooth_weight * 0.2
            self.smooth_weight -= smooth_delta

        self.weight += -BALL_SMALLIZE_SPEED * delta + smooth_delta

    def update(self):
        current_time = time.time()
        delta_time = current_time - self._last_time
        self._last_time = time.time()

        for i in range(len(self._forces) - 1, -1, -1):
            self._forces[i][1] -= delta_time

            if self._forces[i][1] <= 0:
                self._forces.pop(i)

        if not self.mergable and current_time - self._last_merge >= BALL_MERGE_SPAN:
            self.mergable = True

        self._update_movement(delta_time)
        self._update_weight(delta_time)

    def draw(self, target, states):
        target.draw(self._instance, states)
