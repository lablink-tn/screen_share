from socket import socket
from zlib import compress
from mss import mss

WIDTH = 1900
HEIGHT = 1000

def send_screenshot(conn):
    with mss() as sct:
        rect = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT}
        while True:
            img = sct.grab(rect)
            pixels = compress(img.rgb, 6)

            size = len(pixels)
            size_len = (size.bit_length() + 7) // 8
            conn.send(bytes([size_len]))

            size_bytes = size.to_bytes(size_len, 'big')
            conn.send(size_bytes)

            conn.sendall(pixels)

def main(host='0.0.0.0', port=5001):
    sock = socket()
    sock.bind((host, port))
    sock.listen(5)
    print('Server started.')

    while True:
        conn, addr = sock.accept()
        print('Client connected IP:', addr)
        send_screenshot(conn)

if __name__ == '__main__':
    main()
