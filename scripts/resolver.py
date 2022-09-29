# This script runs through each schema and dereferences it. 

import json
import os

def resolve(obj, wd, all_schemas={}, top_level=False):
    if isinstance(obj, list):
        for i, v in enumerate(obj):
            obj[i] = resolve(v, wd, all_schemas)
    elif isinstance(obj, dict):
        if "allOf" in obj:
            # Resolving all those with top-level ref's. We may still need to
            # keep the 'allOf' in case there's non-ref elements in there, e.g.,
            # if/then/else statements. 
            included = []
            other = []
            for v in obj["allOf"]:
                res = resolve(v, wd, all_schemas)
                if "$ref" in v or top_level:
                    included.append(res)
                else:
                    other.append(res)

            if len(included):
                del obj["allOf"]
                obj = fuse([obj] + included)

            if len(other):
                obj["allOf"] = other

        if "$ref" in obj:
            target = os.path.normpath(os.path.join(wd, obj["$ref"]))
            if not target in all_schemas:
                with open(target, "rU") as f:
                    loaded = json.load(f)
                    all_schemas[target] = resolve(loaded, os.path.dirname(target), all_schemas, top_level = ("$id" in loaded))
            obj = all_schemas[target]
        else:
            for k, v in obj.items():
                obj[k] = resolve(v, wd, all_schemas)
    return obj

def fuse(args, handler=None):
    all_lists = [isinstance(obj, list) for obj in args]
    if all(all_lists):
        return sorted(list(set().union(*args)))

    all_dicts = [isinstance(obj, dict) for obj in args]
    if all(all_dicts):
        combined = {}

        for i, x in enumerate(args):
            # Check if we're dealing with a parent reference within a derived
            # class. If so, we only want to fuse particular fields from the
            # parent class. The first object is assumed to contain metadata for
            # the derived class, hence the i > 0 check.
            if "$id" in x and i > 0 and "$id" in args[0]:
                approved = ["properties", "required", "additionalProperties"]
                if "allOf" in x:
                    approved.append("allOf")
                desc = x["description"]
                desc = desc[0].lower() + desc[1:]
                combined["description"] += "\n\nDerived from `" + x["$id"] + "`: " + desc
            else:
                approved = x.keys()

            for k in approved:
                if k in combined:
                    handler2 = None
                    if k == "minItems":
                        handler2 = max
                    elif k == "maxItems":
                        handler2 = min
                    combined[k] = fuse([combined[k], x[k]], handler=handler2)
                else:
                    combined[k] = x[k]

        return combined

    union = set(args)
    if len(union) == 1:
        return union.pop()

    if handler == None:
        raise TypeError("fused values must be all lists, all dictionaries, or all the same value")

    return handler(union)

if __name__ == "__main__":
    import sys
    indir = sys.argv[1]

    outdir = sys.argv[2]
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    import glob
    files = glob.glob(indir + '/**/*.json', recursive=True)
    all_schemas = {}

    for fname in files:
        print("processing " + fname)
        curdir = os.path.dirname(fname)
        dname = os.path.basename(curdir)
        bname = os.path.basename(fname)

        if dname[0] != "_": 
            with open(fname, "rU") as f:
                out = json.load(f)

            out2 = resolve(out, curdir, top_level=True, all_schemas=all_schemas)
            outsubdir = os.path.join(outdir, dname)
            if not os.path.exists(outsubdir):
                os.mkdir(outsubdir)

            with open(os.path.join(outsubdir, bname), 'w', encoding='utf-8') as f:
                json.dump(out2, f, sort_keys=True, ensure_ascii=False, indent=4)
                f.write("\n") # add an extra newline.
