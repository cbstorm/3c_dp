from lib import lbstudio
from label_studio_sdk.data_manager import Filters, Column, Operator, Type
import json


def GetListNewTasks():
    filters = Filters.create(Filters.AND, [
        Filters.item(
            Column.total_annotations,
            Operator.EQUAL,
            Type.Number,
            Filters.value(0)
        ),
        Filters.item(
            Column.total_predictions,
            Operator.EQUAL,
            Type.Number,
            Filters.value(0)
        ),
    ])
    response = lbstudio.client.tasks.list(
        project=1, query=json.dumps({"filters": filters}))
    tasks = []
    for t in response:
        tasks += [{
            "id": t.id,
            "image": t.data["image"]
        }]
    return tasks
