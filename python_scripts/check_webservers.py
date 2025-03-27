#!/usr/bin/env python3

import socket
import sys

FILE_PATH = "/usr/local/nagios/libexec/webservers.txt"
PORT = 80
TIMEOUT = 2

def read_server_list(file_path):
    servers = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                if ':' in line:
                    name, ip = line.strip().split(':')
                    servers.append((name, ip))
    except Exception as e:
        print(f"UNKNOWN - Could not read server list: {e}")
        sys.exit(3)
    return servers

def check_servers(servers):
    offline = []
    for name, ip in servers:
        try:
            socket.create_connection((ip, PORT), TIMEOUT).close()
        except:
            offline.append(name)
    return offline

def main():
    servers = read_server_list(FILE_PATH)
    offline = check_servers(servers)

    if len(offline) == 0:
        print("OK - All web servers are online")
        sys.exit(0)
    elif len(offline) == 1:
        print(f"WARNING - One web server offline: {offline[0]}")
        sys.exit(1)
    else:
        print(f"CRITICAL - Both web servers are offline: {', '.join(offline)}")
        sys.exit(2)

if __name__ == '__main__':
    main()
