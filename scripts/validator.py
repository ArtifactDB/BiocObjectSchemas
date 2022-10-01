import jsonschema
import json

if __name__ == "__main__":
    import sys
    indir = sys.argv[1]
    standard = sys.argv[2]
    with open(standard, "r") as handle:
        schema = json.load(handle)

    import glob
    files = glob.glob(indir + '/**/*.json', recursive=True)
    all_schemas = {}

    for fname in files:
        print("validating " + fname)
        with open(fname, "r") as handle:
            instance = json.load(handle)
