import lbstudio
import json


def GetProject():
    p = lbstudio.client.projects.get(id=1)
    return {"id": p.id, "labels": p.parsed_label_config["label"]["labels"]}


def main():
    p = GetProject()
    print(json.dumps({
        "id": p.id,
        "labels": p.parsed_label_config["label"]["labels"],
    }, indent=2))
    # print(p)


if __name__ == '__main__':
    main()
