# coding: utf-8
import sys
import socket


def main(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('0.0.0.0', port))
    print 'listen on %s' % port
    try:
        while True:
            data, addr = s.recvfrom(4096)
            back_msg = 'Your address is %r\n' % (addr,)
            s.sendto(back_msg, addr)
            print 'recvfrom:%s msg:%s' % (addr, data)
    except KeyboardInterrupt:
        return


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'which port?'
    else:
        main(int(sys.argv[1]))
