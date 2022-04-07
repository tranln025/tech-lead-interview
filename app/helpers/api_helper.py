import json
from flask import Response


def return_items(items, offset=0, count=None):
    if count == None:
        count = len(items)

    headers = {
        "Content-Range": "items {}-{}/{}".format(offset, offset + len(items), count)
    }

    return Response(
        json.dumps(items), mimetype="application/json", status=200, headers=headers
    )