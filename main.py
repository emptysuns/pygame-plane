import pygame
import sys
import traceback
import myplane
import enemy
import bullet
import supply
import random
from pygame.locals import *

pygame.init()
pygame.mixer.init()
bg_size = width, height = 400, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("打飞机")
background = pygame.image.load("img/background.png").convert()

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 255)
WHITE = (255, 255, 255)

########################载入游戏音乐########################
pygame.mixer.music.load("sound/game_music1.ogg")
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
button_sound = pygame.mixer.Sound("sound/button.wav")
button_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.2)
enemy3_flying_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_flying_sound.set_volume(0.2)
game_music1_ogg_sound = pygame.mixer.Sound("sound/game_music1.ogg")
game_music1_ogg_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
use_bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
use_bomb_sound.set_volume(0.2)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
########################载入游戏音乐########################

def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)

def add_big_enemies(group1, group2, num):
    for i in range(num):
        e3 = enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)

def inc_speed(target, inc):
    for each in target:
        each.speed += inc
def main():
    pygame.mixer.music.play(-1)
    # 创建主人公飞机
    me = myplane.MyPlane(bg_size)
    # 控制运行的变量
    running = True
    # 设置延迟变量控制飞机两张图片的刷新速度
    delay = 60
    # 控制切换主人公飞机图片
    switch_image = False
    # 将所有敌人飞机放到一个组里面
    enemies = pygame.sprite.Group()
    # 创建敌人小型飞机
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)
    # 创建敌人中型飞机
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 5)
    # 创建敌人大型飞机
    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemies, 2)
    # 创建普通子弹bullet1
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 4
    for each in range(BULLET1_NUM):
        bullet1.append(bullet.Bullte1(me.rect.midtop))

    # 创建超级子弹bullet2
    bullet2 = []
    bullet2_index = 0
    BULLET2_NUM = 8
    for each in range(BULLET2_NUM // 2):
        bullet2.append(bullet.Bullte2((me.rect.centerx - 33, me.rect.centery)))
        bullet2.append(bullet.Bullte2((me.rect.centerx + 30, me.rect.centery)))

    # 创建得分
    score = 0
    score_font = pygame.font.Font("font/font.ttf", 36)

    # 标志暂停
    paused = False
    pause_nor_image = pygame.image.load("img/pause_nor.png").convert_alpha()
    pause_pressed_image = pygame.image.load("img/pause_pressed.png").convert_alpha()
    resume_nor_image = pygame.image.load("img/resume_nor.png").convert_alpha()
    resume_pressed_image = pygame.image.load("img/resume_pressed.png").convert_alpha()
    # 四个图片尺寸相同只需要获得一张图rect就行了
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10
    paused_image = pause_nor_image



    # 中弹索引
    e1_destory_index = 0
    e2_destory_index = 0
    e3_destory_index = 0
    me_destory_index = 0


    # 设置难度级别level
    level = 1

    # 全屏炸弹
    bomb_image = pygame.image.load("img/bomb.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font("font/font.ttf", 48)
    bomb_num = 3

    # 设置30s一个补给包降落
    bullet_supply = supply.Bullet_Supply(bg_size)
    bomb_supply = supply.Bomb_Supply(bg_size)
    SUPPLY_TIME = USEREVENT
    pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)

    # 设计一个超级子弹double的计时器
    DOUBLE_BULLET_TIME = USEREVENT + 1


    # 是否使用超级子弹
    is_double_bullet = False

    # 生命数量
    life_image = pygame.image.load("img/life.png")
    life_rect = life_image.get_rect()
    life_num = 3

    # 复活无敌计时器
    IMVINCIBLE_TIME = USEREVENT + 2

    # 用于组织重复打开记录文件
    recorded = False

    # 绘制结束界面
    gameover_font = pygame.font.Font("font/font.ttf", 48)
    again_image = pygame.image.load("img/again.png").convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load("img/gameover.png").convert_alpha()
    gameover_rect = gameover_image.get_rect()
    clock = pygame.time.Clock()
    while running:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                        pygame.time.set_timer(SUPPLY_TIME, 0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        use_bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False
            # 进行随机生成补给包
            elif event.type == SUPPLY_TIME:
                supply_sound.play()

                if random.choice([True, False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()

            elif event.type == DOUBLE_BULLET_TIME:
                is_double_bullet = False
                pygame.time.set_timer(DOUBLE_BULLET_TIME, 0)
            elif event.type == IMVINCIBLE_TIME:
                me.invincible = False
                pygame.time.set_timer(IMVINCIBLE_TIME, 0)
        # 根据用户得分来判断难度级别
        if level == 1 and score > 50000:
            level = 2
            upgrade_sound.play()
            # 增加三架小型飞机,两架中型飞机,一架大型飞机
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)
            inc_speed(small_enemies, 1)
        elif level == 2 and score > 300000:
            level = 3
            upgrade_sound.play()
            # 增加三架小型飞机,两架中型飞机,一架大型飞机
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
        elif level == 3 and score > 600000:
            level = 4
            upgrade_sound.play()
            # 增加五架小型飞机,三架中型飞机,二架大型飞机
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
        elif level == 4 and score > 1000000:
            upgrade_sound.play()
            # 增加五架小型飞机,三架中型飞机,二架大型飞机
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)


        # 判断是否暂停游戏
        if life_num and not paused:
            ##########检测用户键盘操作##########
            key_pressed = pygame.key.get_pressed()
            # 根据键盘方向判断飞机的移动
            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRight()
            ##########检测用户键盘操作##########
            #绘制补给并进行二者碰撞检测
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, me):
                    get_bomb_sound.play()
                    if bomb_num < 3:
                        bomb_num += 1
                    bomb_supply.active = False

            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, me):
                    get_bullet_sound.play()
                    is_double_bullet = True
                    pygame.time.set_timer(DOUBLE_BULLET_TIME, 18 * 1000)
                    bullet_supply.active = False

            # 发射子弹
            if not (delay % 10):
                button_sound.play()
                if is_double_bullet:
                    bullets = bullet2
                    bullets[bullet2_index].reset((me.rect.centerx - 33, me.rect.centery))
                    bullets[bullet2_index + 1].reset((me.rect.centerx + 30, me.rect.centery))
                    bullet2_index = (bullet2_index + 2) % BULLET2_NUM
                else:
                    bullets = bullet1
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % BULLET1_NUM

            # 检测子弹是否击中敌机
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if e in mid_enemies or e in big_enemies:
                                e.hit = True
                                e.energy -= 1
                                if e.energy == 0:
                                    e.active = False
                            else:
                                e.active = False
            # 绘制分数
            score_text = score_font.render("Score : %s" % str(score), True, WHITE)
            screen.blit(score_text, (10, 5))
            ###################把飞机图像画到画布上######################
            # 生成大型飞机
            for each in big_enemies:
                if each.active:
                    each.move()
                    # 绘制被打到的特效
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        if switch_image:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)
                    #  绘制血槽
                    pygame.draw.line(screen, BLACK, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.right, each.rect.top - 5),\
                                     2)
                    # 当生命大于20%时显示绿色，反之显示红色
                    energy_remain = each.energy / enemy.BigEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.left + each.rect.width * energy_remain, \
                                      each.rect.top - 5), \
                                     2)
                    # 如果即将出现则播放大型飞机专属bgm
                    if each.rect.bottom == -50:
                        enemy3_flying_sound.play(-1)
                else:
                    # 毁灭
                    if (delay % 3):
                        if e3_destory_index == 0:
                            enemy3_down_sound.play()
                        screen.blit(each.destory_images[e3_destory_index], each.rect)
                        e3_destory_index = (e3_destory_index + 1) % 6
                        if e3_destory_index == 0:
                            enemy3_flying_sound.stop()
                            score += 10000
                            each.reset()


            # 生成中型飞机
            for each in mid_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image, each.rect)
                    #  绘制血槽
                    pygame.draw.line(screen, BLACK, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.right, each.rect.top - 5), \
                                     2)
                    # 当生命大于20%时显示绿色，反之显示红色
                    energy_remain = each.energy / enemy.MidEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.left + each.rect.width * energy_remain, \
                                      each.rect.top - 5), \
                                     2)
                else:
                    # 毁灭
                    if (delay % 3):
                        if e2_destory_index == 0:
                            enemy2_down_sound.play()
                        screen.blit(each.destory_images[e2_destory_index], each.rect)
                        e2_destory_index = (e2_destory_index + 1) % 4
                        if e2_destory_index == 0:
                            score += 6000
                            each.reset()

            # 生成小型飞机
            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    # 毁灭
                    if (delay % 3):
                        if e1_destory_index == 0:
                            enemy1_down_sound.play()
                        screen.blit(each.destory_images[e1_destory_index], each.rect)
                        e1_destory_index = (e1_destory_index + 1) % 4
                        if e1_destory_index == 0:
                            score += 1000
                            each.reset()


            # 生成主角驾驶的飞机
            #检测我方飞机是否被撞
            enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
            if enemies_down and me.invincible:
                me.active = True
            elif enemies_down:
                me.active = False
            for e in enemies_down:
                e.active = False
            if me.active:
                if switch_image:
                    screen.blit(me.image1, me.rect)
                else:
                    screen.blit(me.image2, me.rect)
            else:
                # 毁灭
                if (delay % 3):
                    if me_destory_index == 0:
                        me_down_sound.play()
                    screen.blit(me.destory_images[me_destory_index], me.rect)
                    me_destory_index = (me_destory_index + 1) % 4
                    if me_destory_index == 0:
                        life_num -= 1
                        me.reset()
                        pygame.time.set_timer(IMVINCIBLE_TIME, 3 * 1000)
            # 绘制炸弹:
            bomb_text = bomb_font.render("x %d" % bomb_num, True, WHITE)
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
            screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 -text_rect.height))

            # 绘制飞机生命数量
            if life_num:
                for each in range(life_num):
                    screen.blit(life_image, \
                                (width - 10 - (each + 1)*life_rect.width, \
                                 height - 10 - life_rect.height))

        # 绘制游戏失败
        elif life_num == 0:
            # 背景音乐停止
            pygame.mixer.music.stop()
            # 停止全部音效
            pygame.mixer.stop()
            # 停止发放补给
            pygame.time.set_timer(SUPPLY_TIME, 0)

            if not recorded:
                # 读取记录文件
                recorded = True
                with open("recoder.txt", "r") as f:
                    record_score = int(f.read())
                # 如果分数是最高分则记录
                if score > record_score:
                    with open("recoder.txt", "w") as f:
                        f.write(str(score))

            # 绘制结束画面
            record_score_text = score_font.render("Best : %d" % record_score, True, (255, 255, 255))
            screen.blit(record_score_text, (50, 50))

            gameover_text1 = gameover_font.render("Your Score", True, (255, 255, 255))
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = \
                (width - gameover_text1_rect.width) // 2, height // 3
            screen.blit(gameover_text1, gameover_text1_rect)

            gameover_text2 = gameover_font.render(str(score), True, (255, 255, 255))
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = \
                (width - gameover_text2_rect.width) // 2, \
                gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)

            again_rect.left, again_rect.top = \
                (width - again_rect.width) // 2, \
                gameover_text2_rect.bottom + 50
            screen.blit(again_image, again_rect)

            gameover_rect.left, gameover_rect.top = \
                (width - again_rect.width) // 2, \
                again_rect.bottom + 10
            screen.blit(gameover_image, gameover_rect)
            # 检测用户的鼠标操作
            # 如果用户按下鼠标左键
            if pygame.mouse.get_pressed()[0]:
                # 获取鼠标坐标
                pos = pygame.mouse.get_pos()
                # 如果用户点击“重新开始”
                if again_rect.left < pos[0] < again_rect.right and \
                        again_rect.top < pos[1] < again_rect.bottom:
                    # 调用main函数，重新开始游戏
                    main()
                # 如果用户点击“结束游戏”
                elif gameover_rect.left < pos[0] < gameover_rect.right and \
                        gameover_rect.top < pos[1] < gameover_rect.bottom:
                    # 退出游戏
                    pygame.quit()
                    sys.exit()




        #绘制暂停按钮
        screen.blit(paused_image, paused_rect)

        if not (delay % 5):
            switch_image = not switch_image
        delay -= 1
        if not delay:
            delay = 60
        ###################把飞机图像画到画布上######################
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit
        input()
