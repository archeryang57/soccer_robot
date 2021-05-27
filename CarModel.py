import pygame

import numpy as np

from Ball import Ball

import random


class CarModel(pygame.sprite.Sprite):


    # const 參數
    # 最大轉向角度
    max_steering_angle = np.pi/4

    # 最大速度
    maxSpeed = 10.0

    # 加速度
    accelerate = 0.05

    # 最大煞車速度
    maxBrakeSpeed = 5.0

    # 煞車速率
    brakerate = 0.0

    # 油門 0 ~ 1 
    throttle = 0.5

    # 檔位, 0:空檔 1:前進 -1:後退
    gearshift = 1.0

    # 狀態
    # 車輛長度
    car_length = 60.0

    # 下一步的x,y差異值(斜率分量)
    dx = 0.0 
    dy = 0.0

    # 速度 ( 速度' = 速度 + (油門*加速度) - (最大煞車速度 * 煞車速率)    #暫時不算檔位
    speed = 0.0

    # 車頭方向(角度)
    orientation = 2.0 * np.pi

    # 車輪角度
    steering_angle = np.pi / 8


    def __init__(self, color, initial_position):
        pygame.sprite.Sprite.__init__(self)
        self.orig_image = pygame.image.load('car.png').convert()
        self.image = self.orig_image
        self.car_length = self.image.get_height()
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position

        self.dx = 0.0
        self.dy = 0.0

        self.display_width, self.display_height = pygame.display.get_surface().get_size()
        self.ball_list = []
        self.point_list = []


    def set_car(self, x, y, orientation, steering_angle):
        self.orientation = orientation
        self.steering_angle = steering_angle

        self.image = self.setCarImage()

        self.rect.centerx = x
        self.rect.centery = y
        self.dx = 0.0
        self.dy = 0.0
        self.point_list.append((x,y))


    def calculate_speed(self):

        # 暫時不算檔位
        speed = self.speed + (self.throttle * self.accelerate) - (self.maxBrakeSpeed * self.brakerate)

        if speed > self.maxSpeed * self.throttle:
            speed = self.maxSpeed * self.throttle
        elif speed < 0.0:
            speed = 0.0
        return speed


    def update(self):
        self.move()
        for ball in self.ball_list:
            if pygame.sprite.collide_mask(self, ball):
                self.kick_ball(ball)


    def move(self):
        # 取得下一個位置及車輛角度
        _x, _y, _theta = self.next_step()

        # 計算dx,dy 車子與球的斜率分量(計算球的移動速度用)
        dx = _x - self.rect.centerx
        dy = _y - self.rect.centery

        deno = abs(dx) if abs(dx) > abs(dy) else abs(dy)
        if deno != 0:
            self.dx = dx / deno
            self.dy = dy / deno

        # 存入計算點並畫軌跡線
        self.point_list.append((_x,_y))
        self.draw_track()

        # 更新車輛位置及角度
        self.orientation = _theta
        self.image = self.getRotatedImage()
        self.rect = self.image.get_rect()
        self.rect.centerx = _x
        self.rect.centery = _y


    def next_step(self):
        # 計算速度
        self.speed = self.calculate_speed() # self.maxSpeed * self.throttle
        theta = self.orientation # 車輛目前方向
        alpha = self.steering_angle # 車輛轉向
        dist = self.speed # 移動距離
        length = self.car_length # 車輛長度(應是前後輪軸長度)

        # 計算移動後與原點的夾角
        beta = (dist/length)*np.tan(alpha)
        # beta = np.arctan(1.2*np.tan(theta)/self.car_length)

        cx = cy = radius = 0.0
        if beta > 0.001 or beta < -0.001:
            # 算出轉彎半徑
            radius = dist/beta 

            # 計算圓心及新的位置
            # cx = self.rect.centerx - radius * np.sin(theta)
            # cy = self.rect.centery - radius * np.cos(theta)
            # _x = cx + radius * np.sin(theta + beta) + 0.5
            # _y = cy + radius * np.cos(theta + beta) + 0.5

            # 新位置另一種算法, 用dist做斜邊來運算,不必計算圓心位置
            # sin(theta) = (y-y') / dist   ;   cos(theta) = (x'-x) / dist
            _x = self.rect.centerx + dist * np.cos(theta) + 0.5
            _y = self.rect.centery - dist * np.sin(theta) + 0.5

            _theta = (theta + beta)%(2*np.pi)  # 移動後車輛的角度

        else:
            _x = self.rect.centerx + dist * np.cos(theta)
            _y = self.rect.centery + dist * np.sin(theta)
            _theta = self.orientation # 角度不變
        
        # print(f"beta={beta}  R={radius}, cx={cx}, cy={cy}, cos(theta)={np.cos(theta)}")

        return (_x, _y, _theta)


    def getRotatedImage(self):
        return pygame.transform.rotate(self.orig_image, (self.orientation*180/np.pi)-90)


    def draw_track(self):
        (x,y) = self.point_list[0]
        for (_x,_y) in self.point_list:
            pygame.draw.line(pygame.display.get_surface(),(0, 0, 0),(x, y),(_x,_y), 1)
            (x,y) = (_x, _y)


    def increase_speed(self, step=0.1):
        self.set_throttle(self.throttle + step)


    def decrease_speed(self, step=0.1):
        self.set_throttle(self.throttle - step)


    def set_throttle(self, throttle):
        if throttle > 1.0:
            self.throttle = 1.0
        elif throttle < 0.0:
            self.throttle = 0.0
        else:
            self.throttle = throttle


    def turn_left(self, step=np.pi/32):
        self.set_steeringAngle(self.steering_angle + step )


    def turn_right(self, step=np.pi/32):
        self.set_steeringAngle(self.steering_angle - step )


    def set_steeringAngle(self, steeringAngle ):
        if steeringAngle > self.max_steering_angle :
            self.steering_angle = self.max_steering_angle
        elif steeringAngle < -self.max_steering_angle:
            self.steering_angle = -self.max_steering_angle
        else:
            self.steering_angle = steeringAngle


    def add_ball(self, ball):
        self.ball_list.append(ball)


    def kick_ball(self, ball):
        init_x = self.dx * 2 if abs(self.dx) < 0.1 else self.dx
        init_y = self.dy * 2 if abs(self.dy) < 0.1 else self.dy

        ball.dx = init_x + random.random()/5
        ball.dy = init_y + random.random()/5
        ball.move_step = self.speed * 2

