import ball
import graphics
import utility


PLAYER_SHOT_LIMIT = 15
PLAYER_SPLIT_LIMIT = 30


class Player(graphics.Drawable):
    """Player is a list of balls"""
    def __init__(self, position = None, color = None, id = None):
        super(Player, self).__init__()

        self.balls = [ball.Ball(
            position = position,
            color = color,
            id = id
        )]

    def shot(self):
        L = []

        for ball in self.balls:
            if ball.weight >= PLAYER_SHOT_LIMIT:
                L.append(ball.split(1))

        return L

    def split(self):
        length = len(self.balls)

        for i in range(0, length):
            ball = self.balls[i]

            if ball.weight >= PLAYER_SHOT_LIMIT:
                ball.mergable = False
                self.balls[-1].mergable = False
                self.balls.append(ball.split(ball.weight / 2))

    def try_eat(self, food):
        for ball in self.balls:
            if utility.length(food.position - ball.position) <= ball.radius:
                ball.smooth_weight += food.weight
                return True

        return False

    def set_direction(self, position):
        for ball in self.balls:
            ball.direction = position

    def update(self):
        for i in range(0, len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                ia = i
                ib = j
                a = self.balls[ia]
                b = self.balls[ib]

                if a.mergable and b.mergable:
                    continue

                if a.weight < b.weight:
                    a, b = b, a
                    ia, ib = ib, ia

                if 0.2 <= utility.length(a.position - b.position) <= a.radius + b.radius:
                    b.temporary_forces.append(
                        utility.normalize(b.position - a.position) * (a.weight / (a.weight + b.weight))
                    )
                    a.temporary_forces.append(
                        utility.normalize(a.position - b.position) * (b.weight / (a.weight + b.weight))
                    )

        for ball in self.balls:
            ball.update()

        cnt = [0] * len(self.balls)
        for i in range(0, len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                ia = i
                ib = j
                a = self.balls[i]
                b = self.balls[j]

                if cnt[i] < 0 or cnt[j] < 0:
                    continue

                if a.weight < b.weight:
                    a, b = b, a
                    ia, ib = ib, ia

                if utility.length(a.position - b.position) <= a.radius / 2:
                    if a.mergable and b.mergable:
                        cnt[ia] += b.weight
                        cnt[ib] = -1

        new = []
        for i in range(0, len(cnt)):
            if cnt[i] >= 0:
                self.balls[i].smooth_weight += cnt[i]
                new.append(self.balls[i])
        self.balls = new

    def draw(self, target, states):
        for ball in self.balls:
            target.draw(ball, states)
