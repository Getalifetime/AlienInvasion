
class Settings():
    '存储游戏所有设置的类'

    def __init__(self):
        '初始化游戏的静态设置'
        # 屏幕设置
        self.screen_width = 800
        self.screen_height = 600
        # 设置背景色  红(255,0,0) 绿(0,255,0) 蓝(0,0,255)
        self.bg_color = (230, 230, 230)

        # 飞船的设置        
        self.ship_limit = 3 # 生命数

        # 子弹设置        
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255, 0, 0#60, 60, 60     
        self.auto_fire = False # 自动发射子弹

        # 外星飞船设置
        self.alien_moving_mode = 2 # 外星飞船移动方式 1左右移动并下落 2 随机下落                  

        # 游戏加速
        self.speedup_scale = 1.1

        # 得分点数的提高速度
        self.score_scale = 1.5 # 未使用，目前采用每次+10分

        # 初始化动态设置
        self.initialize_dynamic_settings()
        
    
    def initialize_dynamic_settings(self):
        '初始化随游戏进行而变化的设置'               
        self.fleet_drop_speed = 5 # 外星飞船的设置 
        #self.total_alien_one_level = 30 # 每一级的外星飞船总数 
        #self.total_alien_current = 0    # 每一级已经出现的外星飞船数量
        self.ship_speed_factor = 0.5 # 需要移动飞船时，我们将移动xx像素
        self.bullet_speed_factor = 1
        self.alien_speed_factor = 0.3            

        self.bullets_once = 1 # 一次发射几颗子弹
        self.bullets_once_copy = 1 # 一次发射几颗子弹副本
        self.bullets_allowed = 3 # 限制屏幕中总子弹数
        self.fleet_direction = 1 # 1右移 -1左移 

        self.alien_points = 50 # 射杀每个外星人计分

    def increase_speed(self):
        '提高速度设置'
        #self.ship_speed_factor *= self.speedup_scale # 飞船速度暂时恒定
        #self.bullet_speed_factor += self.speedup_scale 
        #self.alien_speed_factor *= self.speedup_scale 
        self.fleet_drop_speed += self.speedup_scale 

        self.alien_points += 10

        # 子弹随之升级
        if self.bullets_once < 5:
            self.bullets_once += 1
            self.bullets_once_copy = self.bullets_once
        self.bullets_allowed = self.bullets_once * 3

