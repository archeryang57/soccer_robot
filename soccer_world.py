
import pygame
import sys
import math
import tkinter as tk
from Ball import Ball
from CarModel import CarModel
# from CarModelOrig import CarModel
from Door import Door

speed = 30
friction = 0.1
robot_step = 1

screen_width = 800
screen_height = 600


def set_speed(scale_value):
    global speed
    speed = int(scale_value)

def robot_speed(scale_value):
    global robot_step
    robot_step = int(scale_value)

def set_friction(scale_value):
    global friction
    friction = float(scale_value)

def config_window():
    window = tk.Tk()
    window.wm_title("arg settings")
    window.minsize(width=screen_width, height=screen_height)
    window.maxsize(width=screen_width, height=screen_height)
    scale = tk.Scale(window, from_=0, to=120, command=set_speed,
                     orient="horizontal", label='speed', length=screen_height)
    scale.set(speed)
    scale.pack()

    scale2 = tk.Scale(window, from_=0, to=1, command=set_friction,
                     orient="horizontal", label='friction', length=screen_height, resolution=0.01)
    scale2.set(friction)
    scale2.pack()

    scale3 = tk.Scale(window, from_=1, to=20, command=robot_speed,
                     orient="horizontal", label='robot speed', length=screen_height, resolution=1)
    scale3.set(robot_step)
    scale3.pack()


    button = tk.Button(window, text="Start Game", height=5, width=20, command=lambda: main())
    button.pack()

    window.mainloop()

def drawLine(disp, ball, robot):
    pygame.draw.line(disp, start_pos=(ball.rect.x+ball.radius,ball.rect.y+ball.radius), 
                    end_pos=(robot.rect.x+robot.rect.width/2, robot.rect.y+robot.rect.height/2), color=[128,128,0])
    
def main():
    display_width = screen_width
    display_height = screen_height
    white = (255, 255, 255)
    green = (0, 255, 0)
    blue = (0, 0, 128)

    pygame.init()
    clock = pygame.time.Clock()
    display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("Robot_World!")

    ball = Ball([0, 255, 0], [100, 100])
    ball2 = Ball([0, 128, 0], [100, 200])
    ball.friction = friction
    ball2.friction = friction

    car = CarModel([0, 128, 255], [500, 500])
    car.add_ball(ball)
    car.add_ball(ball2)
    car.speed = robot_step

    door = Door([255, 0, 0], [0, 120])

    group = pygame.sprite.Group()
    group.add(car)
    group.add(ball)
    group.add(ball2)
    group.add(door)

    font = pygame.font.Font('freesansbold.ttf', 12)

    pause = False
    while True:
        clock.tick(speed)

        pygame.key.set_repeat(10)
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_SPACE:
                    pygame.time.delay(5000)
                if event.key == pygame.K_UP:
                    car.increase_speed()
                if event.key == pygame.K_DOWN:
                    car.decrease_speed()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    car.turn_left()
                if event.key == pygame.K_RIGHT:
                    car.turn_right()

            if event.type == pygame.QUIT:
                pygame.quit()

        display.fill(white)
        group.update()

        if pygame.sprite.collide_rect(door, ball):
            ball.x = door.rect.width
            ball.dx = abs(ball.dx)
            print("Score")

        group.draw(display)
    
        text = font.render(f'robot_x:{round(car.rect.x,2)}, robot_y:{round(car.rect.y,2)}, robot speed:{round(car.speed,2)}', 
            True, blue, white)
        textRect = text.get_rect().center = (0 , display_width//2 )
        display.blit(text, textRect)
        # drawLine(display, ball, car)
        pygame.display.update()

        # from datetime import datetime
        # dateTimeObj = datetime.now()
        # timeStr = dateTimeObj.strftime("%H%M%S%f")
        # pygame.image.save(display, timeStr +".jpeg")


if __name__ == "__main__":
    # main()
    config_window()
