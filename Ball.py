# 乒乓球物件
# 相關全域參數移到物件內
# 球的移動, 碰撞偵測等程式全部移到物件內
# 新增調整球的移動速度函式

import pygame
import sys


class Ball(pygame.sprite.Sprite):
    def __init__(self, color, initial_position):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 10
        self.image = pygame.Surface([self.radius*2, self.radius*2])
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))
        self.color = color
        self.speed = 0
        self.dx = 0
        self.dy = 0
        self.x_dir = 1
        self.y_dir = 1
        self.friction = 0.02
        pygame.draw.circle(self.image, self.color,
                           (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.display_width, self.display_height = pygame.display.get_surface().get_size()

    def update(self):
        self.dx = self.dx - self.friction if self.dx - self.friction >= 0 else 0
        self.dy = self.dy - self.friction if self.dy - self.friction >= 0 else 0
        self.rect.x += self.dx * self.x_dir
        self.rect.y += self.dy * self.y_dir

        if self.rect.x <= 0:
            self.x_dir = 1

        if self.rect.x >= self.display_width - self.rect.width:
            self.rect.x = self.display_width - self.rect.width
            self.x_dir = -1

        if self.hit_sides():
            self.y_dir *= -1


    def hit_sides(self):
        if self.rect.y <= 0:
            self.rect.y = 0
            return True
        elif self.rect.y + self.rect.height >= self.display_height:
            self.rect.y = self.display_height - self.rect.height
            return True

        return False


