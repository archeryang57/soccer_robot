
import pygame
import sys
import math
import tkinter as tk
from Ball import Ball
from Robot import Robot
from Door import Door

speed = 30
friction = 0.2


def set_speed(scale_value):
    global speed
    speed = int(scale_value)

def set_friction(scale_value):
    global friction
    friction = float(scale_value)

def config_window():
    window = tk.Tk()
    window.wm_title("arg settings")
    window.minsize(width=400, height=300)
    window.maxsize(width=400, height=300)
    scale = tk.Scale(window, from_=0, to=120, command=set_speed,
                     orient="horizontal", label='speed', length=300)
    scale.set(speed)
    scale.pack()
    button = tk.Button(window, text="Start Game", height=5, width=20, command=lambda: main())
    button.pack()
    scale2 = tk.Scale(window, from_=0, to=0.5, command=set_friction,
                     orient="horizontal", label='sin', length=300, resolution=0.01)
    scale2.set(0.1)
    scale2.pack()
    window.mainloop()

def drawLine(disp, ball, robot):
    pygame.draw.line(disp, start_pos=(ball.rect.x+ball.radius,ball.rect.y+ball.radius), 
                    end_pos=(robot.rect.x+robot.rect.width/2, robot.rect.y), color=[128,128,0])
    
def main():
    display_width = 500
    display_height = 300

    pygame.init()
    clock = pygame.time.Clock()
    display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("Robot_World!")

    ball = Ball([0, 255, 0], [100, 100])
    ball2 = Ball([0, 128, 0], [100, 200])
    ball.friction = friction
    ball2.friction = friction

    robot = Robot([0, 128, 255], [40, 40])
    robot.add_ball(ball)
    robot.add_ball(ball2)

    door = Door([255, 0, 0], [0, 120])

    group = pygame.sprite.Group()
    group.add(robot)
    group.add(ball)
    group.add(ball2)
    group.add(door)

    while True:
        clock.tick(speed)

        pygame.key.set_repeat(10)
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    robot.move_up()
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    robot.move_down()
                if event.key == pygame.K_LEFT:
                    robot.move_left()
                if event.key == pygame.K_RIGHT:
                    robot.move_right()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

            if event.type == pygame.QUIT:
                pygame.quit()

        if pygame.sprite.collide_rect(door, ball):
            print("Score")

        display.fill((255, 255, 255))
        group.update()
        group.draw(display)
        # drawLine(display, ball, robot)
        pygame.display.update()

        # from datetime import datetime
        # dateTimeObj = datetime.now()
        # timeStr = dateTimeObj.strftime("%H%M%S%f")
        # pygame.image.save(display, timeStr +".jpeg")


if __name__ == "__main__":
    # main()
    config_window()