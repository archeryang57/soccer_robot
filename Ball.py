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
        self.move_step = 0.0
        self.dx = 0.0
        self.dy = 0.0
        self.friction = 0.02
        pygame.draw.circle(self.image, self.color,
                           (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.x, self.y = self.rect.center
        self.display_width, self.display_height = pygame.display.get_surface().get_size()

    def update(self):
        self.x += self.dx * self.move_step # * self.x_dir
        self.y += self.dy * self.move_step # * self.y_dir
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if self.rect.x <= 0:
            self.rect.x = 10
            self.x = float(self.rect.centerx)
            self.dx = -self.dx
        elif self.rect.x >= self.display_width - self.rect.width:
            self.rect.x = self.display_width - self.rect.width - 10
            self.x = float(self.rect.x)
            self.dx = -self.dx

        if self.rect.y <= 0:
            self.rect.y = 10
            self.y = float(self.rect.centery)
            self.dy = -self.dy
        elif self.rect.y + self.rect.height >= self.display_height:
            self.rect.y = self.display_height - self.rect.height - 10
            self.y = float(self.rect.y)
            self.dy = -self.dy

        self.move_step = self.move_step - self.friction if self.move_step - self.friction > 0 else 0




