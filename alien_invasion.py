import sys

import pygame
from pygame.sprite import Group
from alien import Alien

from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import game_functions as gf


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    # 初始化屏幕参数
    ai_settings = Settings()
 
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height)) 
    # 对象screen是一个surface，表示整个游戏窗口
    # 在pygame中，surface是屏幕的一部分，用于显示屏幕元素

    pygame.display.set_caption("Alien Invasion")

    # 创建Play按钮
    play_button = Button(ai_settings, screen, "Play")

    # 创建一艘飞船
    ship = Ship(ai_settings, screen, 64)
    # 创建一个用于存储子弹的编组
    bullets = Group() #用于存储所有有效的子弹，以便能够管理发射出去的所有子弹
    # 创建一个外星飞船编组
    aliens = Group()
    # 创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)
    # 创建记分牌实例
    sb = Scoreboard(ai_settings, screen, stats)


    # 游戏一开始先创建一个外星舰队
    if ai_settings.alien_moving_mode == 1:
        gf.create_fleet(ai_settings, screen, ship, aliens)

    # 开始游戏主循环
    while True:

        # 监视键盘和鼠标事件
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

        if stats.game_active and not stats.lost_ship:
            # 更新飞船动作
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)
          
        # 绘制和更新屏幕
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)
        

run_game()