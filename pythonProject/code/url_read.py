import json

with open('shuu_url.json') as f:
    List = json.loads(f.read())
    print(List)
