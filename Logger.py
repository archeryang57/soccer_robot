import csv
import os
from CarModel import CarModel
from datetime import datetime

class Logger:
    def __init__(self):
        self.log_number = 1
        self.log_path = './log/'
        self.filename = datetime.strftime(datetime.now(),'%Y%m%d%H%M%S')
        self.create_img_directory()

        csvfile = open(self.log_path + self.filename + "/_log.csv", 'w+', newline='') # 'w+': write with newline
        self.writer = csv.writer(csvfile)
        self.writer.writerow(['No.', 'accelerate', 'brakerate', 'throttle', 'gearshift', 
                'speed', 'orientation', 'steering_angle', 
                'car_x', 'car_y', 'car_dx', 'car_dy' ])

    def create_img_directory(self):
        if os.path.isdir(self.log_path + self.filename)==False:
            os.mkdir(self.log_path + self.filename)

    def get_log_img_filename(self):
        return self.log_path + self.filename + "/" + str(self.log_number) + ".png"

    def save_log(self, car: CarModel):
        # 寫入title
        self.writer.writerow([
            self.log_number,
            car.accelerate,
            car.brakerate,
            car.throttle,
            car.gearshift,
            car.speed,
            car.orientation,
            car.steering_angle,
            car.x,
            car.y,
            car.dx,
            car.dy
        ])
        self.log_number += 1
        
