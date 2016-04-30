import os
import json

def load_json(path):
    jsonFile = open(path)
    data = json.load(jsonFile)
    jsonFile.close()

    return data

def write_json(data,path):
    with open(path, "w") as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False, sort_keys=True)
