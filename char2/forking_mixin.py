"""
使用 socketserver 模块，fork和thread两个类可以实现非同步，分别继承对应的fork/thread类以及
tcp/udp类，
实例化服务器的时候引入一个handler类，其中实现了handle方法
新开一个子线程，并将父线程设置为其守护线程，一方面不会相互影响，另一方面可以自动的结束子线程
"""

import socket
import os
import socketserver
import threading

SERVER_HOST = 'localhost'
SERVER_PORT = 0  # 让套接字自动选择合适的端口
BUF_SIZE = 1024
ECHO_MESSAGE = b'Hello echo server!'


class ForkingClient():
    def __init__(self, ip, port):
        self.sock = socket.socket()
        self.sock.connect((ip, port))

    def run(self):
        current_process_id = os.getpid()
        print('pid %s sending message to server: %s' % (current_process_id, ECHO_MESSAGE))
        send_data_length = self.sock.send(ECHO_MESSAGE)
        print('Send %d chars, so far...' % send_data_length)

        response = self.sock.recv(BUF_SIZE)
        print('pid %s received: %s' % (current_process_id, response[5:]))

    def shutdown(self):
        self.sock.close()


class ForkingServerRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(BUF_SIZE)
        current_process_pid = os.getpid()
        response = bytes('%s: %s' % (current_process_pid, data), encoding='utf-8')
        # current_process_id不同，说明内部新创建了一个进程来处理请求
        print("Server sending response [current_process_id: data] = [%s]" %response)
        self.request.send(response)
        return


class ForkingServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


def main():
    server = ForkingServer((SERVER_HOST, SERVER_PORT), ForkingServerRequestHandler)
    ip, port = server.server_address # 得到系统分配的端口
    server_thread = threading.Thread(target=server.serve_forever)
    # 将主线程设置为守护线程，当主线程运行完毕，服务器线程自动关闭
    server_thread.setDaemon(True)
    server_thread.start()
    print('Server loop running pid: %s' % os.getpid())

    # 启动多个客户端
    client1 = ForkingClient(ip, port)
    client1.run()

    client2 = ForkingClient(ip, port)
    client2.run()

    server.shutdown()
    client1.shutdown()
    client2.shutdown()
    server.socket.close()


if __name__ == '__main__':
    main()