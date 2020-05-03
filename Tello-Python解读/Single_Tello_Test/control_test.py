from tello import Tello
import sys,string
from datetime import datetime
import time
from threading import Thread
import pygame
from  pygame.locals import *

command="command"
class UAV(Thread):
    def _init_(self):
        super().__init__()

    def run(self):
        # command="command"
        global command
        print("start")
        while 1:
            # print(command)
            if command=="land":
                tello.send_command(command)
                break
            if command=="wait":
                print("delay")
                time.sleep(0.01)
            else:
                print(command)
                tello.send_command(command)
                command="wait"
            
        

if __name__=='__main__':
    start_time = str(datetime.now())
    tello=Tello()
    t=UAV()
    t.start()

    pygame.init()
    pygame.display.set_caption("Tello")
    size = (600,400) #窗口的大小
    screen= pygame.display.set_mode(size) 
    keys_pressed = pygame.key.get_pressed()
    while 1:
        for event in pygame.event.get(): 
            if event.type==QUIT:
                pygame.quit()                                               # 停止运行Pygame
                sys.exit()
            if event.type==pygame.KEYDOWN:
                # print("!!!!")
                if event.key==pygame.K_x:
                    command="land"
                if event.key==pygame.K_LSHIFT:
                    command="takeoff"
                if event.key==pygame.K_a:
                    command="left 20"
                if event.key==pygame.K_w:
                    command="forward 20"
                if event.key==pygame.K_s:
                    command="back 20"
                if event.key==pygame.K_d:
                    command="right 20"
                if event.key==pygame.K_q:
                    command="up 20"
                if event.key==pygame.K_e:
                    command="down 20"
                if event.key==pygame.K_z:
                    command="cw 30"
                if event.key==pygame.K_c:
                    command="ccw 30"

    log = tello.get_log()  #无人机日志信息
    out = open('log/' + start_time + '.txt', 'w') #打开日志文件
    for stat in log:
        stat.print_stats()  #将所有状态输出,详见stats.py
        str = stat.return_stats()
        out.write(str)

