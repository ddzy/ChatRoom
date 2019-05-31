# uncompyle6 version 3.3.3
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.2 (tags/v3.7.2:9a3ffc0492, Dec 23 2018, 23:09:28) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: d:\��ѧ�γ����\python�������\��ĩ\ChatRoom\client\client.py
# Size of source mod 2**32: 3511 bytes
import socket, threading, json
from cmd import Cmd

class Client(Cmd):
    """
    �ͻ���
    """
    prompt = ''
    intro = '[Welcome] ���������ҿͻ���(Cli��)\n[Welcome] ����help����ȡ����\n'

    def __init__(self):
        """
        ����
        """
        super().__init__()
        self._Client__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._Client__id = None
        self._Client__nickname = None

    def __receive_message_thread(self):
        """
        ������Ϣ�߳�
        """
        while True:
            try:
                buffer = self._Client__socket.recv(1024).decode()
                obj = json.loads(buffer)
                print('[' + str(obj['sender_nickname']) + '(' + str(obj['sender_id']) + ')' + ']', obj['message'])
            except Exception:
                print('[Client] �޷��ӷ�������ȡ����')

    def __send_message_thread(self, message):
        """
        ������Ϣ�߳�
        :param message: ��Ϣ����
        """
        self._Client__socket.send(json.dumps({'type':'broadcast', 
         'sender_id':self._Client__id, 
         'message':message}).encode())

    def start(self):
        """
        �����ͻ���
        """
        self._Client__socket.connect(('127.0.0.1', 8888))
        self.cmdloop()

    def do_login(self, args):
        """
        ��¼������
        :param args: ����
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
                print('[Client] �ɹ���¼��������')
                thread = threading.Thread(target=(self._Client__receive_message_thread))
                thread.setDaemon(True)
                thread.start()
            else:
                print('[Client] �޷���¼��������')
        except Exception:
            print('[Client] �޷��ӷ�������ȡ����')

    def do_send(self, args):
        """
        ������Ϣ
        :param args: ����
        """
        message = args
        print('[' + str(self._Client__nickname) + '(' + str(self._Client__id) + ')' + ']', message)
        thread = threading.Thread(target=(self._Client__send_message_thread), args=(message,))
        thread.setDaemon(True)
        thread.start()

    def do_help(self, arg):
        """
        ����
        :param arg: ����
        """
        command = arg.split(' ')[0]
        if command == '':
            print('[Help] login nickname - ��¼�������ң�nickname����ѡ����ǳ�')
            print('[Help] send message - ������Ϣ��message�����������Ϣ')
        else:
            if command == 'login':
                print('[Help] login nickname - ��¼�������ң�nickname����ѡ����ǳ�')
            else:
                if command == 'send':
                    print('[Help] send message - ������Ϣ��message�����������Ϣ')
                else:
                    print('[Help] û�в�ѯ������Ҫ�˽��ָ��')
# okay decompiling .\client.cpython-37.pyc
