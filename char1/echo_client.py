import socket
import argparse

host = 'localhost'


def echo_client(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_addr = (host, port)
    sock.connect(server_addr)

    # 发送数据
    try:
        message = b"test message. this will be echoed"
        print('sending %s' % message)
        sock.sendall(message)
        # 查找响应
        amount_received = 0
        amount_expected = len(message)
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            print('received: %s' % data)

    except Exception as e:
        print('other exception %s' % str(e))
    finally:
        print('closing connection to the server')
        sock.close()


# echo_client(10086)

if __name__ == '__main__':
    parse = argparse.ArgumentParser(description='socket server example')
    parse.add_argument('--port', action='store', dest='port', type=int, required=True)
    given_args = parse.parse_args()
    port = given_args.port
    echo_client(port)
