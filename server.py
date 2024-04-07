import socket, datetime
import urllib.parse, json
UDP_IP = '127.0.0.1'
UDP_PORT = 5000


def run_server(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    sock.bind(server)
    try:
        while True:
            data, address = sock.recvfrom(2048)
            print(f'Received data: {data.decode()} from: {address}')
            data_parse = urllib.parse.unquote_plus(data.decode())
            print(data_parse)
            with open('storage/data.json', 'r+') as f:
                info = json.load(f)
            data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
            print(data_dict)
            time_now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            info[time_now] = data_dict
            with open('storage/data.json', 'w+') as f:
                json.dump(info, f)
            print(info)
            sock.sendto(data, address)
            print(f'Send data: {data} to: {address}')
    except KeyboardInterrupt:
        print(f'Destroy server')
    finally:
        sock.close()
    
if __name__ == '__main__':
    run_server(UDP_IP, UDP_PORT)