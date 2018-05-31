import nn
import game

import numpy as np

class Bird:
    x_pos = 100
    radius = 15
    def __init__(self):
        self.y_pos = 200
        self.y_vel = 0
        self.y_acc = 0.6
        self.jump_strength = 9

        self.fitness = 0

        # inputs: y position, distance to next obstacle, end of next obstacle
        #  y velocity, gap start position, gap end position
        self.brain = nn.NeuralNet(6, [4, 2], 2)

    def think(self, nextObs):
        norm_yp = self.y_pos / game.screen_size[1]
        norm_dist = (nextObs.x_pos - (Bird.x_pos - Bird.radius)) / (game.screen_size[0] - Bird.x_pos)
        norm_dist_end = (nextObs.x_pos + nextObs.width - (Bird.x_pos - Bird.radius)) / (game.screen_size[0] - Bird.x_pos)
        norm_yv = 2 / (1 + np.exp(-self.y_vel)) - 1
        norm_start = nextObs.gap_y / game.screen_size[1]
        norm_end = (nextObs.gap_y + nextObs.gap_size) / game.screen_size[1]
        output = self.brain.predict([norm_yp, norm_dist, norm_dist_end, norm_yv, norm_start, norm_end])
        #print('No: {} | Yes: {}'.format(output[0], output[1]))
        if output[1] > output[0] and self.y_vel > 0:
            self.y_vel = -self.jump_strength

    def move(self, nextObstacle):
        self.think(nextObstacle)
        self.y_vel += self.y_acc
        self.y_pos += self.y_vel


class Obstacle:
    def __init__(self, y, s, x):
        self.gap_y = y
        self.gap_size = s
        self.x_pos = x
        self.width = 30

print('Entities loaded')
