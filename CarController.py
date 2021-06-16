import numpy as np
from CarModel import CarModel
from Ball import Ball
from Door import Door

class CarController:
    def __init__(self, car: CarModel, ball: Ball, door: Door):
        self.car = car
        self.ball = ball
        self.door = door
        self.back_dir = "back"  # 倒車方向
        self.back_phase = 0  # 倒車階段 0: 正常往前, 1:加速階段, 2:減速階段
        self.back_step = 0   # 倒車步數暫存

    def update(self):
        # 計算與球的角度
        rad = self.cal_ball_theta()
        # 正對球 radius 是 PI (180度)
        if rad >= 0:
            sterring_angle = np.pi - rad
        else:
            sterring_angle = -(np.pi + rad )
        
        # 將方向盤轉向球的方向(超過最大轉角會以最大轉角旋轉)
        self.car.set_steering_angle(sterring_angle)

        # 計算xx步內是否會撞牆(在減速階段不計算)
        hit_step = 999
        if self.back_phase < 2:
            (hit_step, hit_dir) = self.get_step_will_hit_wall(3)

        # 若會撞牆, 往反方向後退xx步, 再往前開.(也考慮到退車會撞牆的情形)
        if hit_step < 999:
            # 設定倒車方向盤方向
            self.back_steering_angle = self.car.max_steering_angle
            if self.car.steering_angle > 0.0:
               self.back_steering_angle = -self.car.max_steering_angle 
            # 檔位打到相反方向
            if self.car.speed > 0:
                self.car.throttle = -abs(self.car.throttle)
            else:
                self.car.throttle = abs(self.car.throttle)
            # 踩剎車
            self.car.brakerate = 0.5
            # 倒退xx步
            self.back_step = 15
            # 倒退減速階段
            self.back_phase = 2
            # 設定車輛前後方向(與牆的反方向)
            if self.car.speed >= 0:
                self.back_dir = "back"
            else:
                self.back_dir = "ahead"

        if self.back_step > 0:
            self.back_step -= 1
            # 方向盤固定往反方向打(之前會先變更steering angel, 這裡改回來)
            self.car.set_steering_angle(self.back_steering_angle) 
            # 
            if self.back_dir == "back": # 須要倒車
                if self.car.speed > 0:  # 還在往前衝
                    self.car.brakerate = 0.5 # 踩剎車 
                else:                   # 已經往後倒車了
                    self.car.brakerate = 0.0 # 鬆剎車
                    self.back_phase = 1  # 開始加速階段
            else:                       
                if self.car.speed < 0:
                    self.car.brakerate = 0.5
                else:
                    self.car.brakerate = 0.0
                    self.back_phase = 1
        else:
            # 向前開
            self.car.throttle = abs(self.car.throttle)
            # 鬆剎車
            self.car.brakerate = 0.0
            # 倒車模式關閉
            self.back_phase = 0

        # print(f"rad:{rad},    sterring_angle:{sterring_angle}")


    def cal_ball_theta(self):
        # v1: 車子移動的向量
        v1 = [self.car.dx, self.car.dy]
        # v2: 以車子為原點, 與球的向量
        v2 = [self.car.x-self.ball.x, self.car.y - self.ball.y]
        rad =self.get_clock_angle(v1, v2)
        
        # deg =np.rad2deg(rad) % 360
        return rad  # , deg

    # 計算兩個向量的夾角
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
    
    # 計算接下來的路徑, 回傳會在接下來第幾步會撞牆(不會的話回傳999)
    def get_step_will_hit_wall(self, test_steps):
        screen_width = self.car.display_width
        screen_height = self.car.display_height
        car_width = self.car.rect.width

        # car: CarModel = self.car.copy()
        self.car.save_status()

        hit_step = 999
        hit_dir = 'none'
        for i in range(test_steps):
            (x,y,theta) = self.car.next_step() 
            self.car.x = x
            self.car.y = y
            self.car.steering_angle = theta
            if x < car_width/2:
                hit_step = i
                hit_dir = 'left'
                break
            if x > screen_width - car_width/2:
                hit_step = i
                hit_dir = 'right'
                break
            if y < car_width/2:
                hit_step = i
                hit_dir = 'up'
                break
            if y > screen_height -  car_width/2:
                hit_step = i
                hit_dir = 'left'
                break

        self.car.load_status()

        return (hit_step, hit_dir)


    
