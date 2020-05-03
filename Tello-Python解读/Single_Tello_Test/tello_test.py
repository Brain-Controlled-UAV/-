from tello import Tello
import sys
from datetime import datetime
import time

start_time = str(datetime.now())

file_name = sys.argv[1]
#sys.argv[1]代表为python提供的第一个参数

f = open(file_name, "r")
commands = f.readlines()

tello = Tello()
for command in commands:
    if command != '' and command != '\n':
        command = command.rstrip()
        #返回删除 string 字符串末尾的指定字符后生成的新字符串

        if command.find('delay') != -1:   #延迟
            sec = float(command.partition('delay')[2])
            #返回一个3元的元组，第一个为分隔符左边的子串，第二个为分隔符本身，第三个为分隔符右边的子串
            print ('delay %s' % sec)
            time.sleep(sec)
            pass
        else:
            tello.send_command(command)#详见Tello.py中send_command函数

log = tello.get_log()#返回Tello的日志列表

out = open('log/' + start_time + '.txt', 'w') #打开日志文件
for stat in log:
    stat.print_stats()  #将所有状态输出,详见stats.py
    str = stat.return_stats()
    out.write(str)
