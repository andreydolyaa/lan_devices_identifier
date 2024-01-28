# main.py

from scanner.scanner import Scanner


def main():
    scanner = Scanner("test")
    print(scanner.discover_devices())


if __name__ == "__main__":
    main()
