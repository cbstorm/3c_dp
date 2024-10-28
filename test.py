import os


def _getModel():
    d = os.listdir("models")
    model_path = 'models/{}/best.pt'.format(d[0])


def main():
    _getModel()


if __name__ == '__main__':
    main()
