import pygame
import numpy as np
from Ball import Ball
import random
import copy

class CarModel(pygame.sprite.Sprite):

# const 參數
    # 最大轉向角度
    max_steering_angle = np.pi/5.0

    # 最大速度
    maxSpeed = 10.0

    # 最大煞車速度
    maxBrakeSpeed = 5.0

    # 車輛長度
    car_length = 60.0

# 變數: 速度變化
    # 加速度
    accelerate = 0.1

    # 煞車速率
    brakerate = 0.0

    # 油門 0 ~ 1 
    throttle = 0.5

    # 檔位, 0:空檔 1:前進 -1:後退
    gearshift = 1.0

    # 速度 ( 速度' = 速度 + (油門*加速度) - (最大煞車速度 * 煞車速率)    #暫時不算檔位
    speed = 0.0

# 變數: 位置及方向
    # 下一步的x,y差異值(斜率分量)
    dx = 0.0 
    dy = 0.0

    # 車頭方向(角度)
    orientation = 2.0 * np.pi

    # 車輪角度
    steering_angle = np.pi / 8.0

    # 車輛位置(浮點數, 原本用centerX(整數), 會造成誤差, 計算新位置時須另補償0.5)
    x = 0.0
    y = 0.0

    def __init__(self, color, initial_position):
        pygame.sprite.Sprite.__init__(self)
        self.orig_image = pygame.image.load('car.png').convert()
        self.image = self.orig_image
        self.car_length = self.image.get_height()*1.0
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.x = self.rect.centerx
        self.y = self.rect.centery

        self.dx = 0.0
        self.dy = 0.0

        self.display_width, self.display_height = pygame.display.get_surface().get_size()
        self.ball_list = []
        self.point_list = []


    def set_car(self, x, y, orientation, steering_angle):
        self.orientation = orientation
        self.steering_angle = steering_angle

        self.image = self.setCarImage()

        self.x = x
        self.y = y
        self.rect.centerx = x
        self.rect.centery = y
        self.dx = 0.0
        self.dy = 0.0
        self.point_list.append((x,y))


    def calculate_speed(self):

        # 暫時不算檔位
        speed = self.speed + (self.throttle * self.accelerate) - (self.maxBrakeSpeed * self.brakerate)

        if abs(speed) > abs(self.maxSpeed * self.throttle):
            speed = self.maxSpeed * self.throttle
        # elif speed < 0.0:
        #     speed = 0.0
        return speed


    def update(self):
        self.move()
        for ball in self.ball_list:
            if pygame.sprite.collide_mask(self, ball):
                self.kick_ball(ball)


    def move(self):
        # 取得下一個位置及車輛角度
        _x, _y, _theta = self.next_step()

        # 計算dx,dy 車子移動斜率分量(計算撞到球後, 球的移動方向用)
        dx = _x - self.x
        dy = _y - self.y

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
        self.x = _x
        self.y = _y


    def next_step(self):
        # 計算速度
        self.speed = self.calculate_speed() # self.maxSpeed * self.throttle
        
        theta = self.orientation # 車輛目前方向
        alpha = self.steering_angle # 車輛轉向
        dist = self.speed # 移動距離
        length = self.car_length # 車輛長度(應是前後輪軸長度)

        # 計算移動後與原點的夾角
        beta = (dist/length)*np.tan(alpha)

        # 計算新的車輛角度
        if abs(beta) > 0.00001:
            _theta = (theta + beta)%(2.0*np.pi)  # 移動後車輛的角度
        else:
            _theta = theta # 角度不變

        # 計算新位置, 用dist做斜邊來運算,不必計算圓心位置
        # cos(theta) = (x'-x) / dist   ;   sin(theta) = (y-y') / dist
        _x = self.x + dist * np.cos(theta) # 若用centerx, 須另 + 0.5 補償
        _y = self.y - dist * np.sin(theta)# + 0.5

        # print(f"beta={beta}  theta={theta}  angle={self.steering_angle}")

        return (_x, _y, _theta)


    def getRotatedImage(self):
        return pygame.transform.rotate(self.orig_image, (self.orientation*180/np.pi)-90)


    def draw_track(self):
        (x,y) = self.point_list[0]
        for (_x,_y) in self.point_list:
            pygame.draw.line(pygame.display.get_surface(),(0, 0, 0),(x, y),(_x,_y), 1)
            (x,y) = (_x, _y)

        # pygame.draw.line(pygame.display.get_surface(),(0,0,255),(self.x, self.y),(self.x+self.dx*100, self.y+self.dy*100))


    def increase_speed(self, step=0.1):
        self.set_throttle(self.throttle + step)


    def decrease_speed(self, step=0.1):
        self.set_throttle(self.throttle - step)


    def set_throttle(self, throttle):
        if throttle > 1.0:
            self.throttle = 1.0
        elif throttle < -1.0:
            self.throttle = -1.0
        else:
            self.throttle = throttle


    def turn_left(self, step=np.pi/32):
        self.set_steering_angle(self.steering_angle + step )


    def turn_right(self, step=np.pi/32):
        self.set_steering_angle(self.steering_angle - step )


    def set_steering_angle(self, steeringAngle ):
        if steeringAngle > self.max_steering_angle :
            self.steering_angle = self.max_steering_angle
        elif steeringAngle < -self.max_steering_angle:
            self.steering_angle = -self.max_steering_angle
        else:
            self.steering_angle = steeringAngle


    def add_ball(self, ball):
        self.ball_list.append(ball)


    def kick_ball(self, ball):
        init_x = self.dx * 2.0 if abs(self.dx) < 0.1 else self.dx
        init_y = self.dy * 2.0 if abs(self.dy) < 0.1 else self.dy

        ball.dx = init_x + random.random()/5
        ball.dy = init_y + random.random()/5
        ball.move_step = self.speed * 2.0

    def copy(self):
        copyobj = CarModel([0, 128, 255], [200, 200])
        for name, attr in self.__dict__.items():
            if hasattr(attr, 'copy') and callable(getattr(attr, 'copy')):
                copyobj.__dict__[name] = attr.copy()
            else:
                copyobj.__dict__[name] = copy.deepcopy(attr)
        return copyobj