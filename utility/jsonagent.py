import json

def GetJson(path):
    f = open(path)
    obj = json.load(f)
    f.close()
    return obj

def SaveJson(dict,path):
    with open(path, "w") as outfile:
        outfile.write(json.dumps(dict))
        outfile.close()