#!/usr/bin/env python3

import socket
import sys
import random

# Configuration variables
HAPROXY_IP = '172.30.0.51'
PUBLIC_IP = '18.237.177.17'
PORT_RANGE_START = 60000
PORT_RANGE_END = 65000
TIMEOUT = 3

def check_haproxy_stickiness(ip, public_ip, port):
    try:
        sock = socket.create_connection((ip, port), TIMEOUT)
        request = f"GET / HTTP/1.1\r\nHost: {public_ip}:{port}\r\nUser-Agent: curl/7.68.0\r\nAccept: */*\r\nConnection: close\r\n\r\n"
        sock.sendall(request.encode())

        response = ""
        # Read until the socket closes
        while True:
            data = sock.recv(4096).decode()
            if not data:
                break
            response += data

        sock.close()

        if "set-cookie: srv=" in response.lower():
            return True, f"OK - HAProxy stickiness working on port {port}"
        else:
            return False, f"CRITICAL - No stickiness cookie detected on port {port}"

    except Exception as e:
        return False, f"CRITICAL - Failed to connect to HAProxy at {ip}:{port}, error: {e}"

def main():
    random_port = random.randint(PORT_RANGE_START, PORT_RANGE_END)
    success, message = check_haproxy_stickiness(HAPROXY_IP, PUBLIC_IP, random_port)

    if success:
        print(message)
        sys.exit(0)
    else:
        print(message)
        sys.exit(2)

if __name__ == '__main__':
    main()
