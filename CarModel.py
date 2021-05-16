import pygame
import numpy as np
from Ball import Ball
from random import random


class CarModel(pygame.sprite.Sprite):

    # const 參數
    # 最大轉向角度
    maxSteeringAngle = pi/4
    # 最大速度
    maxSpeed = 30
    # 加速度
    accelerate = 1.0
    # 最大煞車速度
    maxBrakeSpeed = 5
    # 煞車速率
    brakerate = 0

    theta = 0.5
    delta = 5
    beta = 5
    L = 2
    lr = 1.2
    w_max = 1.22
        
    sample_time = 1

    # 油門 0 ~ 1 
    throttle = 0.0
    # 檔位, 0:空檔 1:前進 -1:後退
    gearshift = 0
    # 加速計算
    # speed = speed + ( maxSpeed * throttle * gearshift *(accelerate/maxSpeed) - (maxBrakeSpeed*brakerate)
    # speed = maxSpeed if speed > maxSpeed else speed
    # speed = 0.0 if speed < 0.0 else speed

    # 狀態
    # 位置
    dx = 0.0  # 要有小數點, 計算移動距離用
    dy = 0.0
    # 速度 ( speed = speed + ( maxSpeed * throttle * gearshift *(accelerate/maxSpeed) )
    speed = 0
    # 車頭方向(角度)
    heading = 0
    # 車輪角度
    steering_angel = 0
    # 圓心
    xc = 300
    yc = 200

    def set_steering_angle(self, angle):
        self.steering_angel = angle

    def set_gearshift(self, shift):
        self.gearshift = shift

    def set_throttle(self, throttle):
        self.throttle = throttle
    
    def set_brakerate(self, brakerate):
        self.brakerate = brakerate

    def calculate_speed(self):
        self.speed = self.speed + ( self.maxSpeed * self.throttle * self.gearshift *
            (self.accelerate / self.maxSpeed )) - (self.maxBrakeSpeed * self.brakerate)

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
        self.speed = 5
        self.ball_list = []
        self.dx = 0.0
        self.dy = 0.0

	def set_car(self, x, y, orientation, steering_angle):

		# if x >= self.display_width or x < 0:
		# 	raise ValueError('X coordinate out of bound')
		# if y >= self.display_height or y < 0:
		# 	raise ValueError('Y coordinate out of bound')
		# if orientation >= 2*pi or orientation < 0:
		# 	raise ValueError('Orientation must be in [0..2pi]')
		# if abs(steering_angle) > max_steering_angle:
		#     raise ValueError('Exceeding max steering angle')

		self.rect.x = x
		self.rect.y = y
		self.orientation = orientation
		self.steering_angle = steering_angle

    def set_linear_x(self, linear_x):
        self.linear_x = linear_x

    def set_angular_z(self, angular_z):
        self.angular_z = angular_z

    def increase_speed(self, step=1):
        self.speed += step

    def decrease_speed(self, step=1):
        self.speed -= step

    def add_ball(self, ball):
        self.ball_list.append(ball)

    def update(self):
        # self.move()
        self.step(np.pi, self.speed)
        for ball in self.ball_list:
            if pygame.sprite.collide_mask(self, ball):
                self.kick_ball(ball)

    def step(self, v, w):
        self.xc=self.xc+self.sample_time*(v*np.cos(self.theta+self.beta))
        self.yc=self.yc+self.sample_time*(v*np.sin(self.theta+self.beta))
        self.theta=self.theta+self.sample_time*((v*np.cos(self.beta)*np.tan(self.delta))/self.L)
        self.delta=self.delta+self.sample_time*(w)
        self.beta=np.arctan(self.lr*np.tan(self.delta)/self.L)
        
        self.rect.x = self.xc
        self.rect.y = self.yc

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

        next_x = self.rect.x + self.dx * self.speed
        next_y = self.rect.y + self.dy * self.speed

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
        ball.move_step = self.speed * 2
