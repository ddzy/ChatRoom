# uncompyle6 version 3.3.3
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.2 (tags/v3.7.2:9a3ffc0492, Dec 23 2018, 23:09:28) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: d:\大学课程相关\python程序设计\期末\ChatRoom\client\client.py
# Size of source mod 2**32: 3511 bytes
import socket, threading, json
from cmd import Cmd

class Client(Cmd):
    """
    客户端
    """
    prompt = ''
    intro = '[Welcome] 简易聊天室客户端(Cli版)\n[Welcome] 输入help来获取帮助\n'

    def __init__(self):
        """
        构造
        """
        super().__init__()
        self._Client__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._Client__id = None
        self._Client__nickname = None

    def __receive_message_thread(self):
        """
        接受消息线程
        """
        while True:
            try:
                buffer = self._Client__socket.recv(1024).decode()
                obj = json.loads(buffer)
                print('[' + str(obj['sender_nickname']) + '(' + str(obj['sender_id']) + ')' + ']', obj['message'])
            except Exception:
                print('[Client] 无法从服务器获取数据')

    def __send_message_thread(self, message):
        """
        发送消息线程
        :param message: 消息内容
        """
        self._Client__socket.send(json.dumps({'type':'broadcast', 
         'sender_id':self._Client__id, 
         'message':message}).encode())

    def start(self):
        """
        启动客户端
        """
        self._Client__socket.connect(('127.0.0.1', 8888))
        self.cmdloop()

    def do_login(self, args):
        """
        登录聊天室
        :param args: 参数
        """
        nickname = args.split(' ')[0]
        self._Client__socket.send(json.dumps({'type':'login', 
         'nickname':nickname}).encode())
        try:
            buffer = self._Client__socket.recv(1024).decode()
            obj = json.loads(buffer)
            if obj['id']:
                self._Client__nickname = nickname
                self._Client__id = obj['id']
                print('[Client] 成功登录到聊天室')
                thread = threading.Thread(target=(self._Client__receive_message_thread))
                thread.setDaemon(True)
                thread.start()
            else:
                print('[Client] 无法登录到聊天室')
        except Exception:
            print('[Client] 无法从服务器获取数据')

    def do_send(self, args):
        """
        发送消息
        :param args: 参数
        """
        message = args
        print('[' + str(self._Client__nickname) + '(' + str(self._Client__id) + ')' + ']', message)
        thread = threading.Thread(target=(self._Client__send_message_thread), args=(message,))
        thread.setDaemon(True)
        thread.start()

    def do_help(self, arg):
        """
        帮助
        :param arg: 参数
        """
        command = arg.split(' ')[0]
        if command == '':
            print('[Help] login nickname - 登录到聊天室，nickname是你选择的昵称')
            print('[Help] send message - 发送消息，message是你输入的消息')
        else:
            if command == 'login':
                print('[Help] login nickname - 登录到聊天室，nickname是你选择的昵称')
            else:
                if command == 'send':
                    print('[Help] send message - 发送消息，message是你输入的消息')
                else:
                    print('[Help] 没有查询到你想要了解的指令')
# okay decompiling .\client.cpython-37.pyc
