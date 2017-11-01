import socket
import argparse
import sys

host = 'localhost'
data_payload = 2048
backlog = 5


def echo_server(port):
    """一个简单的回显服务器"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 允许重用套接字地址
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = (host, port)
    print("start echo server on host %s port %s" % server_address)
    sock.bind(server_address)
    sock.listen(backlog)
    while True:
        print("waiting to receive message from client")
        client, addr = sock.accept()
        data = client.recv(data_payload)
        if data:
            print('data: %s' % data)
            client.send(data)
            print('sent %s bytes back to %s' % (data, addr))
        client.close()


if __name__ == "__main__":
    parse = argparse.ArgumentParser(description='Socket server example')
    parse.add_argument('--port', action="store", dest='port', type=int, required=True)
    given_args = parse.parse_args()
    port = given_args.port
    echo_server(port)

