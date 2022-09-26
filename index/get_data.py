import requests
import json
import time

# URL = "https://api.slin.dev/grab/v1/list?max_format_version=6&type=ok"
URL = "https://api.slin.dev/grab/v1/list?max_format_version=6"
TS = ""
DATA = []
l = 1
while l > 0:
    r = requests.get(URL+TS)
    if r.status_code == 200:
        if TS != "&timestamp="+r.json()[len(r.json()) - 1]["page_timestamp"]:
            TS = "&timestamp="+r.json()[len(r.json()) - 1]["page_timestamp"]
            DATA.extend(r.json())
            print("Got {} items".format(len(r.json())))
            print("Last timestamp: {}".format(r.json()[len(r.json()) - 1]["page_timestamp"]))
            print("page: " + str(l))
            l += 1
            with open("temp.json", "a") as f:
                json.dump(r.json(), f, indent=4)
        else:
            print("No new data")
            break
    else:
        l = 0
    # time.sleep(5)

with open("data.json", "w") as f:
    json.dump(DATA, f, indent=4)