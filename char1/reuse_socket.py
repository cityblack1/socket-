import socket
import sys


def reuse_socket_addr():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 默认就已经是了

    # 查看旧的重用状态
    old_state = sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
    print("old sock state is %s" % old_state)

    # 使用重用功能
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    new_state = sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
    print("new sock state is %s" % new_state)

    local_port = 10086

    # 重新建立一个socket实例作为服务器
    srv = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(('', local_port))
    srv.listen(1)
    print('Listening on port %s' %local_port)
    while True:
        try:
            connection, addr = srv.accept()
            print('Connected by %s:%s' % (addr[0], addr[1]))
        except KeyboardInterrupt:
            break
        except socket.error as msg:
            print('%s' % msg)

if __name__ == "__main__":
    reuse_socket_addr()

