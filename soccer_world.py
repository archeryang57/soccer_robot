
from CarController import CarController, DriveMode, DriveState
import pygame
import tkinter as tk
from Logger import Logger
from Ball import Ball
from CarModel import CarModel
from Door import Door

speed = 30
friction = 0.15
robot_step = 1
throttle = 0.8

screen_width = 800
screen_height = 600
display_width = screen_width
display_height = screen_height

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)


def set_throttle(throttle_value):
    global throttle
    throttle = float(throttle_value)

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
                     orient="horizontal", label='robot initial speed', length=screen_height, resolution=1)
    scale3.set(robot_step)
    scale3.pack()

    scale4 = tk.Scale(window, from_=0, to=1, command=set_throttle,
                     orient="horizontal", label='car trottle', length=screen_height, resolution=0.1)
    scale4.set(throttle)
    scale4.pack()


    button = tk.Button(window, text="Start Game", height=5, width=20, command=lambda: main())
    button.pack()

    window.mainloop()

def draw_path(path):
    if len(path) > 1:
        (x,y) = path[0]
        for (_x,_y) in path:
            pygame.draw.line(pygame.display.get_surface(),(255, 0, 0),(x, y),(_x,_y), 1)
            (x,y) = (_x, _y)

def draw_points(way_point, color):
    if len(way_point) > 0:
        for pos in way_point:
            pygame.display.get_surface().fill(color, (pos, (4, 4)))

def reset_car(car:CarModel):
    car.x = 200.0
    car.y = 200.0
    # car.dx = 0.0
    # car.dy = 0.0
    # car.orientation = 0.0
    # car.gearshift = 1.0
    # car.speed = 0.0

def reset_ball(ball:Ball):
    ball.x = 400.0
    ball.y = 280.0
    # ball.dx = 0.0
    # ball.dy = 0.0
    # ball.speed = 0.0

def ball_in_corners(ball:Ball):
    ret = False
    if ball.speed == 0:
        if ball.rect.top <= 10 or ball.rect.bottom >= screen_height - 10:
            if ball.rect.left <= 10 or ball.rect.right >= screen_width - 10:
                ret = True

    return ret

def main():
    pygame.init()
    clock = pygame.time.Clock()
    display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("Robot_World!")

    ball = Ball([0, 255, 0], [400, 200])
    ball.friction = friction
    # ball2 = Ball([0, 128, 0], [100, 200])
    # ball2.friction = friction

    car = CarModel([0, 128, 255], [600, 400])
    car.speed = robot_step
    car.set_throttle(throttle)

    door = Door([255, 0, 0], [0, screen_height/2 - 60])

    group = pygame.sprite.Group()
    group.add(car)
    group.add(ball)
    # group.add(ball2)
    group.add(door)

    controller = CarController(car, ball, door)
    logger = Logger()

    font = pygame.font.Font('freesansbold.ttf', 12)

    pause = False
    while True:
        clock.tick(speed)

        pygame.key.set_repeat(10)
        events = pygame.event.get()
        
        controller.update()

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

        if ball_in_corners(ball):
            # reset_car(car)
            reset_ball(ball)

        if controller.drive_mode == DriveMode.BY_PATH:
            draw_path(controller.temp_path)
            draw_points(controller.way_point, green)
        else:
            if controller.drive_state == DriveState.NORMAL:
                draw_path(controller.temp_path)
                # draw_points(controller.way_point, green)
                # path, way_point = controller.get_bezier_path()
                # draw_path(path)
                # draw_points(way_point, blue)

        if pygame.sprite.collide_rect(door, ball):
            ball.x = door.rect.width
            ball.dx = abs(ball.dx)
            # reset_car(car)
            reset_ball(ball)
            print("Score")

        if pygame.sprite.collide_mask(car, ball):
            car.kick_ball(ball)
            controller.temp_path = []

        group.draw(display)
    
        pygame.display.update()
        # show_text(font, display)

        pygame.image.save(display, logger.get_log_img_filename() )
        logger.save_log(car)

def show_text(font, display, car):
    import math
    text = font.render(f'car orientation:{round(car.orientation,4)}, \
car.degrees:{round(math.degrees(car.orientation),2)},  car speed:{round(car.speed,2)}', 
        True, blue, white)
    textRect = text.get_rect().topleft = (10 , display_height-20 )
    display.blit(text, textRect)


if __name__ == "__main__":
    # main()
    config_window()
