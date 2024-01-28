import socket
import struct
import platform
import os
import subprocess
from typing import List


class Scanner:
    _DNS_IP = "8.8.8.8"
    _DNS_PORT = 80
    _TEMP_PORTS_LIST = [
        80,
        433,
        21,
        22,
        25,
        23,
        53,
        3389,
        110,
        143,
        8080,
        3389,
        3306,
        5005,
    ]

    def __init__(self, name: str):
        self.name = name
        self.local_network_ip = ""
        self.devices = []

    def _get_local_network_ip(self) -> str:
        try:
            print("Getting local network IP...")
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((self._DNS_IP, self._DNS_PORT))
            self.local_network_ip = s.getsockname()[0]
            return self.local_network_ip
        except socket.error as e:
            print(f"Error: {e}")
        finally:
            s.close()

    def _ping_host(self, ip: str) -> bool:
        try:
            param = "-n" if platform.system().lower() == "windows" else "-c"
            command = ["ping", param, "1", "-W", "1", ip]
            output = subprocess.check_output(
                command, stderr=subprocess.STDOUT, universal_newlines=True
            )
            print(f"Ping Output for {ip}: {output}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Unreachable Destination {ip}: {e.output}")
            return False

    def discover_devices(self, ip_range: List[int] = None) -> List[object]:
        self._get_local_network_ip()
        if self.local_network_ip is None:
            print("Unable to find local IP")
            return []

        ip_prefix = ".".join(self.local_network_ip.split(".")[:-1])

        for i in range(98, 115):
            ip_to_scan = f"{ip_prefix}.{i}"
            # if ip_to_scan != self.local_network_ip and self.ping_host(ip_to_scan):
            print(ip_to_scan)
            if self._ping_host(ip_to_scan):
                open_ports = self._scan_ports(ip_to_scan, self._TEMP_PORTS_LIST)
                if open_ports:
                    print("Found Ports: ", open_ports)
                    self.devices.append(
                        {"ip": ip_to_scan, "mac": "N/A", "open_ports": open_ports}
                    )
                else:
                    self.devices.append({"ip": ip_to_scan, "mac": "N/A"})

        return self.devices

    def _scan_ports(self, target_ip: str, ports: List[int]) -> List[int]:
        open_ports = []
        print("Scanning for open ports...")
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target_ip, port))
            if result == 0:
                banner = self._test_open_port_for_banner(target_ip, port)
                print(banner)
                open_ports.append(port)
            sock.close()
        return open_ports

    def _test_open_port_for_banner(self, ip: str, port: int):
        # TODO: fix
        return None
        # try:
        #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #         s.settimeout(2)
        #         s.connect((ip, port))
        #         s.sendall(b"GET / HTTPS/1.1\r\n\r\n")
        #         banner = s.recv(1024).decode("utf-8")
        #     return banner
        # except (socket.error, socket.timeout):
        #     return None


# TODO: add argparse
# TODO: set ports list & ip range as cli args
