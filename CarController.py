import numpy as np
from CarModel import CarModel
from Ball import Ball
from Door import Door

class CarController:
    def __init__(self, car: CarModel, ball: Ball, door: Door, screen_width, screen_height):
        self.car = car
        self.ball = ball
        self.door = door
        self.back_mode = False
        self.back_step = 0
        self.screen_width = screen_width   # 計算是否會撞牆用(暫未用到)
        self.screen_height = screen_height

    def update(self):
        rad = self.cal_ball_theta()
        # 正對球 radius 是 PI (180度)
        if rad >= 0:
            sterring_angle = np.pi - rad
        else:
            sterring_angle = -(np.pi + rad )
        
        self.car.set_steering_angle(sterring_angle)
        # 計算xx步內是否會撞牆
        (hit_step, hit_dir) = self.get_step_will_hit_wall(5)

        # 若會撞牆, 往反方向後退xx步, 再往前開.
        if hit_step < 999:
            # 記下方向盤方向
            self.temp_steering_angle = self.car.steering_angle
            # 打倒檔
            self.car.throttle = -self.car.throttle
            # 方向盤切到反方向
            self.car.set_steering_angle(-self.car.steering_angle)
            # 踩剎車
            self.car.brakerate = 0.5
            # 開啟倒退模式
            self.back_mode = True
            # 倒退5步
            self.back_step = 5
        elif self.back_step > 0:
            self.back_step -= 1
            # 方向盤固定往反方向打(之前會先變更steering angel, 這裡改回來)
            self.car.set_steering_angle(-self.temp_steering_angle) 
            # brakerate 目前實作是減少speed, speed 小於0再減下去會變成倒車加速, 所以設0
            if self.car.speed <= 0: 
                self.car.brakerate = 0
        elif self.back_mode == True and self.back_step <= 0:  # 完成倒退
            # 向前開
            self.car.throttle = abs(self.car.throttle)
            # 鬆剎車
            self.car.brakerate = 0.0
            # 倒車模式關閉
            self.back_mode = False

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
    def get_step_will_hit_wall(self, count):
        screen_width = 800
        screen_height = 600
        car_width = 30
        car_height = 60

        car: CarModel = self.car.copy()

        hit_step = 999
        hit_dir = 'none'
        for i in range(count):
            (x,y) = self.next_step(car)
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

        return (hit_step, hit_dir)


    def next_step(self, car):
        # 計算速度
        car.speed = car.calculate_speed() # self.maxSpeed * self.throttle
        
        theta = car.orientation # 車輛目前方向
        alpha = car.steering_angle # 車輛轉向
        dist = car.speed # 移動距離
        length = car.car_length # 車輛長度(應是前後輪軸長度)

        # 計算移動後與原點的夾角
        beta = (dist/length)*np.tan(alpha)

        # 計算新的車輛角度
        if abs(beta) > 0.00001:
            _theta = (theta + beta)%(2.0*np.pi)  # 移動後車輛的角度
        else:
            _theta = theta # 角度不變

        # 計算新位置, 用dist做斜邊來運算,不必計算圓心位置
        # cos(theta) = (x'-x) / dist   ;   sin(theta) = (y-y') / dist
        _x = car.x + dist * np.cos(theta) # 若用centerx, 須另 + 0.5 補償
        _y = car.y - dist * np.sin(theta)# + 0.5
        
        # 更新 car 到下個位置及角度
        car.x = _x
        car.y = _y
        car.orientation = _theta

        return (_x, _y)


    
