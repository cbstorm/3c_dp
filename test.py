import os
import re


def sorted_alphanumeric(data):
    def convert(text): return int(text) if text.isdigit() else text.lower()
    def alphanum_key(key): return [convert(c)
                                   for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)


def main():
    dir = "tmp/vid_0"
    files = sorted_alphanumeric(os.listdir(dir))
    with open("tmp/vid_list.txt", "a") as f:
        for fi in files:
            f.write("file '{}'\n".format("./vid_0/{}".format(fi)))


if __name__ == '__main__':
    main()
