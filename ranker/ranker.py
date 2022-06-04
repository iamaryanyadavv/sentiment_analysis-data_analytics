import json

def ranker(file):
    def foo(e):
        return e["rating"]

    f = open(file)
            
    data = json.load(f)

    arr = []
    for i in data["hotels"]:
        arr.append({ "name" : i["name"], "rating" : i["overall_rating"]})
    f.close()

    arr.sort(reverse=True, key=foo)
    
    return arr[:10]


