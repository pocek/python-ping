#!/usr/bin/env python3
import argparse
import os
import socket
import time

from icmp import IcmpEcho

class Target:

    def __init__(self, target):
        self.name = target
        try:
            res = socket.getaddrinfo(target, None, socket.AF_INET)
        except socket.gaierror as e:
            raise argparse.ArgumentTypeError('Error looking up {target}: {error}'.format(target=target, error=str(e))) from e
        if len(res) == 0:
            raise argparse.ArgumentTypeError('Error looking up {target}: No addresses returned for target')
        self.address = res[0][4]

    def __str__(self):
        return '{name} [{address}]'.format(name=self.name, address=self.address[0])

def ping(target, timeout=5.0):
    request = IcmpEcho(payload=os.urandom(32))
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_ICMP) as s:
        s.connect(target.address)
        s.settimeout(timeout)

        start = time.clock_gettime(time.CLOCK_MONOTONIC)
        s.send(request.to_bytes())
        response = s.recv(65536)
        end = time.clock_gettime(time.CLOCK_MONOTONIC)

    response = IcmpEcho.from_bytes(response)
    rtt_ms = (end - start) * 1000
    print('Got response in {delay:.3f} ms'.format(delay=rtt_ms))

def parse_args():
    parser = argparse.ArgumentParser(description='Simple Python ping script')
    parser.add_argument('target', type=Target, help='Ping target')
    return parser.parse_args()

def main():
    args = parse_args()
    print('Sending ping to:', args.target)
    ping(args.target)

if __name__ == '__main__':
    main()
