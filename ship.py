import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen, image_size):
        '初始化飞船并设置其初始位置'
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #加载飞船图像并获取其外接矩形
        if image_size == 64:
            self.image = pygame.image.load('images/ship64.png')
        elif image_size == 36:
            self.image = pygame.image.load('images/ship36.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #移动标志
        self.moving_right = False
        self.moving_left = False

        # Pygame的效率之所以如此高，一个原因是它让你能够像处理矩形（rect对象）一样处理游戏元素，即便它们的形状并非矩形。
        # 像处理矩形一样处理游戏元素之所以高效，是因为矩形是简单的几何形状。
        # 这种做法的效果通常很好，游戏玩家几乎注意不到我们处理的不是游戏元素的实际形状

        # 将每艘飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        # 处理rect对象时，可使用矩形四角和中心的x和y坐标。可通过设置这些值来指定矩形的位置。
        # 要将游戏元素居中，可设置相应rect对象的属性center、centerx或centery。
        # 要让游戏元素与屏幕边缘对齐，可使用属性top、bottom、left或right；
        # 要调整游戏元素的水平或垂直位置，可使用属性x和y，它们分别是相应矩形左上角的x和y坐标。
        # 这些属性让你无需去做游戏开发人员原本需要手工完成的计算，你经常会用到这些属性

        # 在Pygame中，原点(0, 0)位于屏幕左上角，向右下方移动时，坐标值将增大。
        # 在1200×800的屏幕上，原点位于左上角，而右下角的坐标为(1200, 800)

        # 在飞船的属性center中存储小数值
        self.center = float(self.rect.centerx)

    def blitme(self):
        '在指定位置绘制飞船'
        self.screen.blit(self.image, self.rect)

    def update(self):
        """根据移动标志调整飞船的位置""" 
        # rect的centerx等属性只能存储整数值
        # 更新飞船的center值，而不是rect 
        if self.moving_right and self.rect.right < self.screen_rect.right: 
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0: 
            self.center -= self.ai_settings.ship_speed_factor
        
        # 根据self.center更新rect对象
        self.rect.centerx = self.center 
    
    def center_ship(self):
        '让飞船在屏幕上居中'
        self.center = self.screen_rect.centerx