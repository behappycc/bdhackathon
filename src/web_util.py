import os
import json
import sys
#reload(sys)
#sys.setdefaultencoding(sys.getfilesystemencoding())
def load_json(path):
    jsonFile = open(path,encoding='utf8')
    data = json.load(jsonFile)
    jsonFile.close()

    return data

def write_json(data,path):
    with open(path, "w") as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False, sort_keys=True).encode('utf8')
