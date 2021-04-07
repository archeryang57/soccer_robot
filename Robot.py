import pygame
import numpy as np
from Ball import Ball
from random import random


class Robot(pygame.sprite.Sprite):
    def __init__(self, color, initial_position):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface([6, 40])
        self.orig_image = pygame.image.load('car.png').convert()
        self.image = self.orig_image
        # self.image.fill(color)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.linear_x = 0
        self.angular_z = 0
        self.display_width, self.display_height = pygame.display.get_surface().get_size()
        self.move_step = 5
        self.ball_list = []
        self.dx = 0.0
        self.dy = 0.0
      
    def move_up(self):
        if self.rect.y - self.move_step >= 0:
            self.rect.y -= self.move_step
            
    def move_down(self):
        if self.rect.y + self.rect.height + self.move_step <= self.display_height:
            self.rect.y += self.move_step

    def move_left(self):
        if self.rect.x - self.move_step >= 0:
            self.rect.x -= self.move_step
            
    def move_right(self):
        if self.rect.x + self.rect.width + self.move_step <= self.display_width:
            self.rect.x += self.move_step

    def set_linear_x(self, linear_x):
        self.linear_x = linear_x

    def set_angular_z(self, angular_z):
        self.angular_z = angular_z

    def increase_speed(self, step=1):
        self.move_step += step

    def decrease_speed(self, step=1):
        self.move_step -= step

    def add_ball(self, ball):
        self.ball_list.append(ball)

    def update(self):
        self.move()
        for ball in self.ball_list:
            if pygame.sprite.collide_mask(self, ball):
                self.kick_ball(ball)

    def move(self):
        ball = self.ball_list[0]
        (x1,y1) = (ball.rect.x+ball.radius, ball.rect.y+ball.radius)
        (x2,y2) = (self.rect.x+self.rect.width/2, self.rect.y+self.rect.height/2)
        dx = x1 - x2
        dy = y1 - y2

        deno = abs(dx) if abs(dx) > abs(dy) else abs(dy)
        if deno != 0:
            self.dx = dx / deno
            self.dy = dy / deno

        next_x = self.rect.x + self.dx * self.move_step
        next_y = self.rect.y + self.dy * self.move_step

        self.image = pygame.transform.rotate(self.orig_image, self.cal_angle())
        self.rect = self.image.get_rect()
        self.rect.x = next_x
        self.rect.y = next_y
        # self.center = (self.rect.x + self.rect.width /2, self.rect.y + self.rect.height /2 )

    def cal_angle(self):
        x1,y1 = (0.0,1.0)
        x2,y2 = (self.dx, self.dy)
        dot = x1*x2 + y1*y2
        det = x1*y2 - y1*x2
        theta = np.arctan2(det, dot)
        theta = theta if theta>0 else 2*np.pi+theta
        return 180 - (theta*180/np.pi)

    def kick_ball(self, ball):
        init_x = self.dx * 2 if abs(self.dx) < 0.1 else self.dx
        init_y = self.dy * 2 if abs(self.dy) < 0.1 else self.dy

        ball.dx = init_x + random()/5
        ball.dy = init_y + random()/5
        ball.move_step = self.move_step * 2