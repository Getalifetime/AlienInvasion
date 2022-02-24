import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '表示单个外星飞船的类'

    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载外星人图像，并设置其rect属性
        self.image = pygame.image.load('images/alien56x56.png') #'images/gift64x64.png'
        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height 

        # 存储外星人的准确位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def blitme(self):
        '在指定位置绘制外星人'
        self.screen.blit(self.image, self.rect)

    def update(self):
        '移动外星飞船'
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
        #self.y += self.ai_settings.fleet_drop_speed
        #self.rect.y = self.y
    
    def check_edges(self):
        '检测外星飞船是否到屏幕边缘'
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True