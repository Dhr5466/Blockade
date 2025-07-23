# 导包
import random
# Pygame Locals 模块是 Pygame 中一个包含大量常量的模块，这些常量用于定义事件类型、键盘按键、颜色和屏幕特效等
import sys
import time
from collections import deque  # 注：因为在列表中需要频繁添加和删除元素，所以用deque容器代替列表；是因为deque具有高效的插入和删除效率

import pygame
from pygame.locals import *

# 基础设置
Screen_Height = 480
Screen_Width = 600
Size = 20  # 小方格大小
Line_Width = 1

# 整体颜色设置
Light = (100, 100, 100)
# 几种食物的颜色和概率
Green = (84, 255, 159)  # 50% +10分
Blue = (0, 0, 255)  # 25% +20分
Purple = (139, 101, 8)  # 20%+30分
Gold = (255, 215, 0)  # 5% +50分
Score_options = {
    Green: 10,Blue: 20,Purple: 30,Gold:40
}
Back_Ground = (102, 139, 139)  # 背景默认颜色
Dark = (200, 200, 200)  # 蛇的颜色
Black = (0, 0, 0)  # 线的颜色
# 游戏区域的坐标范围
Area_x = (0, Screen_Width // Size - 1)  # 横轴  0到29 30个坐标
# 0是左边界，1是右边界 #注：python中//为整数除法；/为浮点数除法
Area_y = (2, Screen_Height // Size - 1)  # 竖直轴  2到23 22个坐标上面俩格用于显示分数等信息


def initsnake():  # 初始化小蛇用 deque保存位置数据
    snake = deque()
    snake.appendleft((0, Area_y[0]))
    snake.appendleft((1, Area_y[0]))
    snake.appendleft((2, Area_y[0]))  # 开始时的头
    return snake


def CreatNewFood(snake):  # 随机位置
    food_x = random.randint(Area_x[0], Area_x[1])
    food_y = random.randint(Area_y[0], Area_y[1]-1)
    while ((food_x, food_y) in snake):
        food_x = random.randint(Area_x[0], Area_x[1])
        food_y = random.randint(Area_y[0], Area_y[1])
    return (food_x, food_y)


def Random_rarity():  # 随机稀有度
    x = random.randint(1, 100)
    if 1 <= x < 50:
        return Green
    elif 51 <= x < 75:
        return Blue
    elif 76 <= x < 95:
        return Purple
    else:
        return Gold


def next_is_vaile(snake, pos):
    next = (snake[0][0] + pos[0], snake[0][1] + pos[1])
    if (next[0] < Area_x[0]) or (next[0] > Area_x[1]) or (next[1] < Area_y[0]) or (next[1] > Area_y[1] - 1) \
            or (next in snake):  # 越界或撞到自己了
        return False
    return True


def check_pos(snake, pos):
    next = (snake[0][0] + pos[0], snake[0][1] + pos[1])
    if next == snake[1]:
        return False
    return True


def main():
    pygame.init()
    screen = pygame.display.set_mode((Screen_Width, Screen_Height), 0)
    #   flag位置的值
    #   0 用户设置的窗口大小
    #   pygame.FULLSCREEN 创建一个全屏窗口
    pygame.display.set_caption("贪吃蛇开始吃吃吃")
    # 蛇
    snake = initsnake()  # Snake[0]作为头
    # 食物
    food = CreatNewFood(snake)  # 搞新的食物出现
    food_Rarity = Random_rarity()
    # 分数
    score = 0
    # 方向控制
    pos = (1, 0)  ###向下一个方向增加的一个量，默认为向右
    # 设置游戏状态
    game_ready = True  # 游戏可以开始了
    game_over = False  # 显示游戏输了
    game_going = False  # 正在玩游戏
    pause = False  # 暂停
    # 基础游戏属性
    last_move_time = time.time()
    orispeed = 0.3  # 蛇初始速度
    speed = orispeed  # 蛇速度
    last_move_time = time.time()
    # 状态文本

    ready_font = pygame.font.SysFont('SimHei ', 32)  # 定义文本格式
    ready_text = ready_font.render('按回车开始游戏！！', True, (255, 255, 255))
    pause_font = pygame.font.SysFont('SimHei ', 32)  # 定义文本格式
    pause_text = pause_font.render('暂停，按空格继续游戏!', True, (255, 255, 255))  # 使用font.render()函数将文本渲染成一个表面对象
    over_font = pygame.font.SysFont('SimHei ', 32)  # 定义文本格式
    over_text = over_font.render('你失败了，按回车继续游戏!', True, (255, 255, 255))
    score_font = pygame.font.SysFont('SimHei ', 30)
    score_text = score_font.render("得分 : %s" % str(score), True, (255, 255, 255))
    speed_font = pygame.font.SysFont('SimHei ', 30)
    speed_text = speed_font.render("速度 : %s" % str(speed), True, (255, 255, 255))
    while True:
        for event in pygame.event.get():  # 事件响应
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:  # 按键响应
                if event.key == K_RETURN:
                    if game_ready:  # 开始游戏
                        game_ready = False
                        game_going = True
                    if game_over:
                        game_over = False
                        game_going = True
                        # 重置游戏属性
                        score = 0
                        score_text = score_font.render("得分 : %s" % str(score), True, (255, 255, 255))  # 分数变了，重新渲染
                        last_move_time = time.time()
                        orispeed = 0.3  # 蛇初始速度
                        speed = orispeed  # 蛇速度
                        speed_text = speed_font.render("速度 : %s" % str(speed), True, (255, 255, 255))  # 分数变了，重新渲染
                        last_move_time = time.time()
                        # 蛇
                        snake = initsnake()
                        # 食物
                        food = CreatNewFood(snake)  # 搞新的食物出现
                        # 方向控制
                        pos = (1, 0)  ###向下一个方向增加的一个量，默认为向右
                        # 设置游戏状态

                if event.key == K_SPACE:
                    if game_going:  # 暂停
                        game_going = False
                        pause = True
                    elif pause:  # 停止暂停
                        game_going = True
                        pause = False
                if event.key == K_q:  # 何时都可以退出
                    sys.exit()
                if game_going:  # 游戏运行时才进行pos的改变
                    if event.key in (K_LEFT, K_a):
                        if check_pos(snake, (-1, 0)):
                            pos = (-1, 0)
                    if event.key in (K_RIGHT, K_d):
                        if check_pos(snake, (1, 0)):
                            pos = (1, 0)
                    if event.key in (K_UP, K_w):
                        if check_pos(snake, (0, -1)):
                            pos = (0, -1)
                    if event.key in (K_DOWN, K_s):
                        if check_pos(snake, (0, 1)):
                            pos = (0, 1)
        # 填充背景色
        screen.fill(Back_Ground)
        # 画网格线、竖线
        for t_ in range(Size, Screen_Width, Size):  # 竖线
            pygame.draw.line(screen, Black, (t_, Area_y[0] * Size), (t_, Area_y[1] * Size))
        for t_ in range(Size * Area_y[0], Screen_Height, Size):  # 横线
            pygame.draw.line(screen, Black, (0, t_), (Screen_Width, t_))
        # 蛇的爬行过程,游戏进行时
        if game_going:
            curTime = time.time()
            if curTime - last_move_time > speed:  # 过了一定时间就开始移动
                if next_is_vaile(snake, pos):
                    next = (snake[0][0] + pos[0], snake[0][1] + pos[1])
                    if next == food:  # 吃到食物
                        snake.appendleft(next)
                        score+=Score_options[food_Rarity]
                        score_text = score_font.render("得分 : %s" % str(score), True, (255, 255, 255))  # 分数变了，重新渲染
                        # 食物
                        food = CreatNewFood(snake)  # 搞新的食物出现
                        food_Rarity = Random_rarity()
                        # 加速
                        speed = orispeed - 0.03 * (score // 100)
                        speed_text = score_font.render("速度 : %s" % str(speed), True, (255, 255, 255))  # 分数变了，重新渲染
                    else:
                        snake.appendleft(next)
                        snake.pop()
                    last_move_time = curTime
                else:
                    game_going = False
                    game_over = True


        # 画蛇
        for s in snake:
            pygame.draw.rect(screen, Dark, ((s[0] * Size, s[1] * Size), (Size, Size)))  # 在给定的Surface上绘制矩形。

        # 画食物
        pygame.draw.rect(screen, food_Rarity, ((food[0] * Size, food[1] * Size), (Size, Size)))  # 在给定的Surface上绘制矩形。
        # 画分数
        #score_text = score_font.render("得分 : %s" % str(score), True, (255, 255, 255))  # 分数变了，重新渲染
        text_rect = score_text.get_rect()  # 获取文本矩形并设置居中
        text_rect.right = screen.get_rect().right
        screen.blit(score_text, text_rect)  # 将结果绘制出来

        text_rect = speed_text.get_rect()  # 放左上角
        text_rect.right = screen.get_rect().left

        screen.blit(speed_text, (0,0))  # 将结果绘制出来
        #提示文本
        if game_ready:
            text_rect = ready_text.get_rect()  # 获取文本矩形并设置居中
            text_rect.center = screen.get_rect().center
            screen.blit(ready_text, text_rect)
            pygame.display.flip()
        elif pause:
            text_rect = pause_text.get_rect()  # 获取文本矩形并设置居中
            text_rect.center = screen.get_rect().center
            screen.blit(pause_text, text_rect)
            pygame.display.flip()
        elif game_over:
            text_rect = over_text.get_rect()  # 获取文本矩形并设置居中
            text_rect.center = screen.get_rect().center
            screen.blit(over_text, text_rect)
            pygame.display.flip()

        pygame.display.update()


if __name__ == '__main__':
    main()
