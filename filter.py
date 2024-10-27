import os


def main():
    files = os.listdir("images")
    for i, m in enumerate(files):
        if i % 2 != 0:
            os.remove('images/{}'.format(m))


if __name__ == '__main__':
    main()
