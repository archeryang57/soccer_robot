import numpy as np
from CarModel import CarModel
from Ball import Ball
from Door import Door
from enum import IntEnum
 
class DriveState(IntEnum):  # 倒車階段 0:正常往前, 1:倒車減速階段 2:倒車加速階段, 3:減速階段
    NORMAL = 0
    BACK_DEC = 1
    BACK_ACC = 2
    DEC = 3

class CarController:
    brakeForce = 0.1
    def __init__(self, car: CarModel, ball: Ball, door: Door):
        self.car = car
        self.ball = ball
        self.door = door
        self.back_dir = "back"  # 倒車方向
        self.drive_state:DriveState = DriveState.NORMAL
        self.BACK_STEPS = 25 # 每次倒車總步數
        self.back_step = 0   # 倒車步數暫存
        self.car_throttle = car.throttle
        self.back_throttle = -car.throttle
        self.hit_dir = 'head'


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

        hit_step = 999
        # 計算(現在速度+1)步內是否會撞牆(在減速階段不計算)
        if self.drive_state != DriveState.DEC and self.drive_state != DriveState.BACK_DEC:
            (hit_step, self.hit_dir) = self.get_step_will_hit_wall( abs(int(self.car.speed))+2)

        # 若會撞牆, 往反方向後退xx步, 再往前開.(也考慮到退車會撞牆的情形)
        if hit_step < 999:
            self.init_back()
            self.drive_state = DriveState.DEC

        if self.drive_state == DriveState.DEC:  # 先減速將車停住
            self.stop_car()
            if (self.car.gearshift >0 and self.car.speed <= 0) or (self.car.gearshift <0 and self.car.speed >= 0) :
                # 設定倒車方向盤方向
                # self.correct_car_position()
                self.back_steering_angle = self.car.max_steering_angle
                if self.car.steering_angle > 0.0:
                    self.back_steering_angle = -self.car.max_steering_angle 
                # 檔位打到相反方向
                self.car.gearshift = -self.car.gearshift
                self.drive_state = DriveState.BACK_ACC

        if self.drive_state == DriveState.BACK_ACC:  # 倒車加速
            self.process_car_back()
            if self.back_step <= 0:
                self.drive_state = DriveState.BACK_DEC

        if self.drive_state == DriveState.BACK_DEC:  # 倒車減速
            if self.car.speed < 0:  # 車子在向後開的狀態
                self.stop_car()     # 將車停住
            else:           # 已煞住車或車子在向前開的狀態
                self.drive_state = DriveState.NORMAL 

        if self.drive_state == DriveState.NORMAL:
            self.car.throttle = self.car_throttle   # 加油門
            self.car.gearshift = 1.0                # 排檔向前
            self.car.brakerate = 0.0                # 鬆剎車

    def correct_car_position(self):
        screen_width = self.car.display_width
        screen_height = self.car.display_height
        car_width = self.car.car_length
        
        (chk_up, chk_right, chk_left, chk_down)=self.get_hit_length()

        if self.car.x < chk_left:
            self.car.x = chk_left
        if self.car.x > screen_width - chk_right:
           self.car.x = screen_width - chk_right 
        if self.car.y < chk_up:
           self.car.y = chk_up
        if self.car.y > screen_height - chk_down:
            self.car.y = screen_height - chk_down


    def get_hit_length(self):
        chk_width = self.car.car_width /2
        chk_length = self.car.car_length / 2
        orientation = self.car.orientation
        degree = np.rad2deg(orientation)
        dMod = degree % 90

        first_value = (dMod/90) * chk_width + (90-dMod) / 90 * chk_length
        second_value = (dMod/90) * chk_length + (90-dMod) / 90 * chk_width

        chk_up = chk_right = chk_left = chk_down = 0.0
        if self.car.speed >= 0:
            if degree <= 90:
                chk_right = first_value
                chk_up = second_value
            elif degree <= 180:
                chk_up = first_value
                chk_left = second_value
            elif degree <= 270:
                chk_left = first_value
                chk_down = second_value
            else:
                chk_down = first_value
                chk_right = second_value
        else:
            if degree <= 90:
                chk_left = first_value
                chk_down = second_value
            elif degree <= 180:
                chk_down = first_value
                chk_right = second_value
            elif degree <= 270:
                chk_right = first_value
                chk_up = second_value
            else:
                chk_up = first_value
                chk_left = second_value
        return (chk_up, chk_right, chk_left, chk_down)


    def stop_car(self):
        self.car.throttle = 0.0   # 鬆油門
        self.car.brakerate = self.brakeForce  # 踩剎車
 
    def process_car_back(self):
        self.back_step -= 1
        self.car.throttle = self.car_throttle/2  # 加油門
        # 方向盤固定往反方向打(之前會先變更steering angel, 這裡改回來)
        self.car.set_steering_angle(self.back_steering_angle)  
        if self.back_dir == "back": # 須要倒車
            if self.car.speed > 0:  # 還在往前衝
                self.car.brakerate = self.brakeForce # 踩剎車 
            else:                   # 已經往後倒車了
                self.car.brakerate = 0.0 # 鬆剎車
                self.drive_state = DriveState.BACK_ACC  # 開始加速階段
        else:                       
            if self.car.speed < 0:
                self.car.brakerate = self.brakeForce
            else:
                self.car.brakerate = 0.0
                self.drive_state = DriveState.BACK_ACC

    def init_back(self):
        # 倒退xx步
        self.back_step = self.BACK_STEPS
        # 設定車輛前後方向(與牆的反方向)
        if self.car.speed >= 0:
            self.back_dir = "back"
        else:
            self.back_dir = "ahead" # 倒車模式關閉

        # print(f"rad:{rad},    sterring_angle:{sterring_angle}")

    
    # 計算接下來的路徑, 回傳會在接下來第幾步會撞牆(不會的話回傳999)
    def get_step_will_hit_wall(self, test_steps):
        screen_width = self.car.display_width
        screen_height = self.car.display_height
        car_width = self.car.car_length

        # car: CarModel = self.car.copy()
        self.car.save_status()
        chk_width = self.car.car_width /2
        chk_length = self.car.car_length / 2

        chk_up = chk_right = chk_left = chk_down = 0.0
        orientation = 0.0
        degree = 0.0

        hit_step = 999
        hit_dir = 'none'
        for i in range(test_steps):
            self.car.speed = self.car.calculate_speed()
            (x,y,theta) = self.car.next_step()
            self.car.orientation = theta
            self.car.x = x
            self.car.y = y
            
            (chk_up, chk_right, chk_left, chk_down)=self.get_hit_length()

            # self.car.steering_angle = theta
            if x < chk_left:
                hit_step = i
                hit_dir = 'left'
                break
            if x > screen_width - chk_right:
                hit_step = i
                hit_dir = 'right'
                break
            if y < chk_up:
                hit_step = i
                hit_dir = 'up'
                break
            if y > screen_height - chk_down:
                hit_step = i
                hit_dir = 'down'
                break

        self.car.load_status()

        return (hit_step, hit_dir)
