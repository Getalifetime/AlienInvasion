from enum import auto
import numbers
import sys
from tkinter.tix import AUTO

import pygame
from time import sleep
from random import randint
from random import randrange

from bullet import Bullet
from alien import Alien

BLINK_EVENT = pygame.USEREVENT + 0
ALIEN_MOVE_EVENT = pygame.USEREVENT + 1
AUTO_FIRE_EVENT = pygame.USEREVENT + 2


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    '响应按键按下'
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_UP:
        ai_settings.bullets_once = 500 # 发射一发500宽子弹
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    '响应按键松开'
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    '响应按键和鼠标事件'
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
        elif event.type == ALIEN_MOVE_EVENT:
            fleet_move_by_time(ai_settings, aliens)
        elif event.type == BLINK_EVENT:
            sb.blink_surface = next(sb.blink_surfaces)
            sb.blink_times += 1
            if sb.blink_times > 3: #闪烁三次后停止
                sb.cancel_blink_timer()
                if ai_settings.alien_moving_mode == 2: # 随机模式
                    create_fleet(ai_settings, screen, ship, aliens)
        elif event.type == AUTO_FIRE_EVENT:
            fire_bullet(ai_settings, screen, ship, bullets)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y): 
    """在玩家单击Play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y) #检查鼠标单击位置是否在Play按钮的rect内
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False) # 隐藏光标

        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        # 重置记分牌
        sb.prep_score() 
        sb.prep_high_score() 
        sb.prep_level() 
        sb.prep_ships()

        # 清空外星飞船和子弹列表
        aliens.empty()
        bullets.empty()
        
        # 创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens) 
        ship.center_ship() 

            
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    '更新屏幕上的图像，并切换到新屏幕'
    # 用背景色填充屏幕
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen) # 对编组调用draw()时，Pygame自动绘制编组的每个元素，绘制位置由元素的属性rect决定
    #clock = pygame.time.Clock()
    #clock.tick(50)
    sb.show_score()

    if stats.lost_ship:
        sb.show_blink_text()
        #pygame.display.update()
        #clock = pygame.time.Clock()
        #clock.tick(50)

    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '更新子弹的位置，并删除已消失的子弹'
    # 更新子弹动作
    bullets.update()

    # 删除已消失的子弹
    for bullet in bullets.copy(): #使用bullets副本以支持在循环中修改bullets
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # 有子弹击中了外星飞船时删除子弹和外星飞船
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True) #返回一个字典
    
    # 与外星人碰撞的子弹都是字典collisions中的一个键；而与每颗子弹相关的值都是一个列表，其中包含该子弹撞到的外星人。
    if collisions:
        for aliens_collision in collisions.values():
            stats.score +=  ai_settings.alien_points * len(aliens_collision)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0: # < 3
        # 删除现有的子弹并新建一个舰队
        bullets.empty()
        
        create_fleet(ai_settings, screen, ship, aliens)
        
        # 提高等级
        stats.level += 1
        sb.prep_level()
        if stats.level <= 30: #30级以后不再加速
            ai_settings.increase_speed()
        # 暂停
        #sleep(0.5)

def fire_bullet(ai_settings, screen, ship, bullets):
    '如果还没达到限制，就发射一颗子弹'
    offsets = {
        1:[0],
        2:[-10, 10],
        3:[-20, 0, 20],
        4:[-30, -10, 10, 30],
        5:[-40, -20, 0, 20, 40],
    }

    if len(bullets) < ai_settings.bullets_allowed:
        # 创建一次发射的所有子弹，并将其加入到编组bullets中
        if ai_settings.bullets_once <= 5 and ai_settings.bullets_once >= 0:
            for i in range(len(offsets[ai_settings.bullets_once])):
                new_bullet = Bullet(ai_settings, screen, ship, offsets[ai_settings.bullets_once][i]) 
                bullets.add(new_bullet) 
        elif ai_settings.bullets_once > 5:
            new_bullet = Bullet(ai_settings, screen, ship, 600) 
            bullets.add(new_bullet)
            ai_settings.bullets_once = ai_settings.bullets_once_copy # 发射完宽子弹后立即恢复原有子弹模式
        else:
            new_bullet = Bullet(ai_settings, screen, ship, 0) 
            bullets.add(new_bullet)

def create_fleet(ai_settings, screen, ship, aliens):
    '创建外星飞船舰队'
    
    # 创建一个外星飞船对象
    alien = Alien(ai_settings, screen)

    if ai_settings.alien_moving_mode == 2: # 定时随机降落模式        
        create_random_fleet(ai_settings, screen, aliens)
        pygame.time.set_timer(ALIEN_MOVE_EVENT, 300)
    else: #左右移动并下降模式
        # 计算有几行及一行可容纳多少个
        number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
        number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

        # 创建外星飞船
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x): 
                create_alien(ai_settings, screen, aliens, alien_number, row_number)     

    if ai_settings.auto_fire:
        set_auto_fire_timer() #自动发射子弹   

def get_number_aliens_x(ai_settings, alien_width):
    '计算每行可容纳多少外星飞船'
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    '计算屏幕可容纳多少行外星飞船'
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # 创建一个外星并将其加入当前行
    alien = Alien(ai_settings, screen) 
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number 
    alien.rect.x = alien.x 
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien) 

def create_random_fleet(ai_settings, screen, aliens):
    for row_number in range(5):
        numbers_once = randint(2,10)
        for alien_number in range(numbers_once):
            # 创建一个外星并将其加入当前行
            alien = Alien(ai_settings, screen) 
            #alien.x = randint(100,700)
            alien.x = randrange(50, 750, 60)
            alien.rect.x = alien.x 
            alien.rect.y = 50 - 100 * row_number #randrange(-150, -30, 60)
            aliens.add(alien) 
        #ai_settings.total_alien_current += numbers_once

def fleet_move_by_time(ai_settings, aliens):
    '定时将整个外星舰队下移'
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed

def check_fleet_edges(ai_settings, aliens):
    '外星飞船到达屏幕边缘时采取相应措施'
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    '将整个外星舰队下移，并改变移动方向'
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    '响应被外星人撞到的飞船'
    if stats.ships_left > 0:
        stats.ships_left -= 1
        stats.lost_ship = True
        # 设置闪烁提示定时器
        sb.set_blink_timer() 

        # 更新剩余生命数
        sb.prep_ships()

        # 创建一群新的外星飞船，并将自己放在屏幕底部中央
        if ai_settings.alien_moving_mode == 1: # 传统模式
            create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()    

        # 暂停
        # sleep(1.5)
    else:
        sb.ships.empty()
        stats.game_active = False
        pygame.mouse.set_visible(True)

    # 清空列表
    aliens.empty()
    bullets.empty()
    # 取消定时器
    if ai_settings.alien_moving_mode == 2: # 定时随机降落模式
        #ai_settings.total_alien_current = 0
        pygame.time.set_timer(ALIEN_MOVE_EVENT, 0)
    
    if ai_settings.auto_fire:
        cancel_auto_fire_timer() # 取消自动发射子弹
 

def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    '检查是否有外星飞船到达屏幕底部'
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 与飞船被撞击相同处理
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break # 只要检测到有一艘到达屏幕底部就退出循环，防止生命数多减

def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    '更新所有外星飞船的位置'
    if ai_settings.alien_moving_mode != 2:
        check_fleet_edges(ai_settings, aliens)
        aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens): # 检测外星人和飞船之间的碰撞
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
    else:
        # 外星到达屏幕底端的处理
        check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)

def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def set_auto_fire_timer():
    pygame.time.set_timer(AUTO_FIRE_EVENT, 200)

def cancel_auto_fire_timer():
    pygame.time.set_timer(AUTO_FIRE_EVENT, 0)

