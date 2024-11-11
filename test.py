import os


def main():
    command = "ls tmp/vid_0 | sort -V"
    result = os.popen(command).read()


if __name__ == '__main__':
    main()
