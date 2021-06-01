import numpy as np
from CarModel import CarModel
from Ball import Ball
from Door import Door


class CarController:
    def __init__(self, car: CarModel, ball: Ball, door: Door, screen_width, screen_height):
        self.car = car
        self.ball = ball
        self.door = door
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self):
        rad = self.cal_ball_theta()
        # 正對球 radius 是 PI (180度)
        if rad >= 0:
            sterring_angle = np.pi - rad
        else:
            sterring_angle = -(np.pi + rad )
        self.car.set_steering_angle(sterring_angle)
        # print(f"rad:{rad},    sterring_angle:{sterring_angle}")


    def cal_ball_theta(self):
        # v1: 車子移動的向量
        v1 = [self.car.dx, self.car.dy]
        # v2: 以車子為原點, 與球的向量
        v2 = [self.car.x-self.ball.x, self.car.y - self.ball.y]
        rad =self.get_clock_angle(v1, v2)
        
        # deg =np.rad2deg(rad) % 360
        return rad  # , deg

        
    def get_clock_angle(self, v1, v2):
        # 2個向量模的乘積
        TheNorm = np.linalg.norm(v1)*np.linalg.norm(v2)
        # 叉乘
        rho = np.rad2deg(np.arcsin(np.cross(v1, v2)/TheNorm))
        # 點乘
        theta = np.arccos(np.dot(v1,v2)/TheNorm)

        if rho < 0:
            return -theta
        else:
            return theta



    
