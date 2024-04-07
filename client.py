import socket

UDP_IP = '127.0.0.1'
UDP_PORT = 5000



def run_client(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    sock.sendto(data, server)
    data, address = sock.recvfrom(2048)
    sock.close()


if __name__ == '__main__':
    run_client(UDP_IP, UDP_PORT)