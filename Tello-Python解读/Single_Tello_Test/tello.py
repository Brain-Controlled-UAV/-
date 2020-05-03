import socket
import threading
import time
from stats import Stats

#无人机参数
class Tello:  
    def __init__(self):
        self.local_ip = ''
        self.local_port = 8889
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket for sending cmd
        self.socket.bind((self.local_ip, self.local_port))  #套绑定IP和端口

        # thread for receiving cmd ack
        self.receive_thread = threading.Thread(target=self._receive_thread)
        #调用线程模块：target 是函数名字，需要调用的函数；
        self.receive_thread.daemon = True #主线程运行结束时不对这个子线程进行检查而直接退出
        self.receive_thread.start()

        self.tello_ip = '192.168.10.1'
        self.tello_port = 8889
        self.tello_adderss = (self.tello_ip, self.tello_port)
        self.log = []

        self.MAX_TIME_OUT = 15.0

    def send_command(self, command):
        """
        Send a command to the ip address. Will be blocked until
        the last command receives an 'OK'.
        If the command fails (either b/c time out or error),
        will try to resend the command
        :param command: (str) the command to send
        :param ip: (str) the ip of Tello
        :return: The latest command response
        """
        self.log.append(Stats(command, len(self.log))) #添加状态到日志

        self.socket.sendto(command.encode('utf-8'), self.tello_adderss)  #命令发送至无人机
        print ('sending command: %s to %s' % (command, self.tello_ip))

        start = time.time()
        while not self.log[-1].got_response(): #state.py中返回是否有回应的状态
            now = time.time()
            diff = now - start
            if diff > self.MAX_TIME_OUT:
                print ('Max timeout exceeded... command %s' % command)  #连接超时
                # TODO: is timeout considered failure or next command still get executed
                # now, next one got executed
                return
        print ('Done!!! sent command: %s to %s' % (command, self.tello_ip))

    def _receive_thread(self):
        #子线程接受无人机信息
        """Listen to responses from the Tello.

        Runs as a thread, sets self.response to whatever the Tello last returned.

        """
        while True:
            try:
                self.response, ip = self.socket.recvfrom(1024)
                #返回值是（data,address）。其中data是包含接收数据的字符串，address是发送数据的套接字地址
                print('from %s: %s' % (ip, self.response))

                self.log[-1].add_response(self.response)  #日志最后一个状态更新
            except socket.error as exc:
                print ("Caught exception socket.error : %s" % exc)

    def on_close(self):
        pass
        # for ip in self.tello_ip_list:
        #     self.socket.sendto('land'.encode('utf-8'), (ip, 8889))
        # self.socket.close()

    def get_log(self):
        return self.log

