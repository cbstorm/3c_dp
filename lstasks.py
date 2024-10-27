from lib.lstasks import GetListNewTasks
import json


def main():
    tasks = GetListNewTasks()
    print(json.dumps(tasks, indent=2))


if __name__ == '__main__':
    main()
