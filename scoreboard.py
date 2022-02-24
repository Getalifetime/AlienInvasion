import pygame
import pygame.font
import pygame.time
from pygame.surface import Surface 

from pygame.sprite import Group
from itertools import cycle

from ship import Ship

class Scoreboard():
    '显示得分信息的类'

    def __init__(self, ai_settings, screen, stats):
        '初始化得分相关属性'
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        # 得分信息字体设置
        self.text_color = (0, 0, 255)
        self.font = pygame.font.SysFont(None, 28)

        # 准备初始得分图像
        self.prep_score()
        # 准备最高得分
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

        self.prep_blink_text()

    def prep_score(self):
        '将得分转换为一幅渲染的图像'
        # 函数round()通常让小数精确到小数点后多少位，其中小数位数是由第二个实参指定的。
        # 如果将第二个实参指定为负数，round()将圆整到最近的10、100、1000等整数倍
        rounded_score = round(self.stats.score) # 将得分圆整
        if rounded_score > 9999999:
            rounded_score = 9999999
        score_str = "SCORE {:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        # 将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
    
    def prep_level(self): 
        '将等级转换为渲染的图像'
        level_str = "LEVEL {}".format(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.ai_settings.bg_color) 
 
        # 将等级放在得分下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10 
    
    def prep_high_score(self):
        '将最高得分转换为渲染的图像'
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "HIGH {:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color) 
 
        #将最高得分放在屏幕顶部中央
        self.high_score_rect = self.high_score_image.get_rect() 
        self.high_score_rect.centerx = self.screen_rect.centerx 
        self.high_score_rect.top = self.score_rect.top 

    def prep_ships(self):
        '显示余下的飞船生命数'
        self.ships = Group()
        for ship_number in range(self.stats.ships_left + 1):
            ship = Ship(self.ai_settings, self.screen, 36)
            ship.rect.x = 10 + ship_number * (ship.rect.width + 10)
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        '显示得分信息'
        self.screen.blit(self.score_image, self.score_rect)
        # 显示最高分
        self.screen.blit(self.high_score_image, self.high_score_rect) 
        # 显示等级
        self.screen.blit(self.level_image, self.level_rect) 
        # 显示剩余飞船
        self.ships.draw(self.screen)    

    def prep_blink_text(self):
        font = pygame.font.SysFont(None, 80)
        self.on_text_surface = font.render(
            'You lost one ship!', True, pygame.Color('green3')
        )
        self.blink_rect = self.on_text_surface.get_rect()
        self.blink_rect.center = self.screen.get_rect().center
        #self.off_text_surface = Surface(self.blink_rect.size)
        
        self.off_text_surface = font.render(
            'You lost one ship!', True, pygame.Color('red3')
        )
        
        self.blink_surfaces = cycle([self.on_text_surface, self.off_text_surface])
        self.blink_surface = next(self.blink_surfaces) #self.on_text_surface
    
    def show_blink_text(self):
        self.screen.blit(self.blink_surface, self.blink_rect)
        
    def set_blink_timer(self):
        self.blink_times = 0
        #pygame.display.update()
        BLINK_EVENT = pygame.USEREVENT + 0
        pygame.time.set_timer(BLINK_EVENT, 600)
        

    def cancel_blink_timer(self):
        self.stats.lost_ship = False
        #self.blink_times = 0
        BLINK_EVENT = pygame.USEREVENT + 0
        pygame.time.set_timer(BLINK_EVENT, 0)
        


           



        



