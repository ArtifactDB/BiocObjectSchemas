# Unfortunately, json-schema-for-humans is not very bright when it comes to
# allOf and properties/required at the same level. We need to push the
# properties/required into the allOf so that it renders semi-correctly.

import json
import sys

def nest_allOf(incoming):
    if isinstance(incoming, dict):
        if "allOf" in incoming:
            extra = {}
            if "properties" in incoming:
                extra["properties"] = incoming["properties"]
                del incoming["properties"]
            if "required" in incoming:
                extra["required"] = incoming["required"]
                del incoming["required"]
            if extra:
                incoming["allOf"].insert(0, extra)

        for x, v in incoming.items():
            if x != "allOf": 
                incoming[x] = nest_allOf(v)

    elif isinstance(incoming, list):
        for i, v in enumerate(incoming):
            incoming[i] = nest_allOf(v)

    return incoming

incoming = json.load(open(sys.argv[1], 'r'))
outgoing = nest_allOf(incoming)
json.dump(outgoing, open(sys.argv[2], 'w'), sort_keys=True, ensure_ascii=False, indent=4)
