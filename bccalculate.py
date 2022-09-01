from flask import Flask, request, json
from flask_cors import CORS, cross_origin

import requests


from requests.structures import CaseInsensitiveDict
#import json

# <strong>#Set up Flaskstrong>:
app = Flask(__name__)
# <strong>#Set up Flask to bypass CORSstrong>:
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

print("benefit/cost calculation service")

def get_json():
    url="http://localhost:3000/backlog"

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    resp = requests.get(url, headers=headers)
    print(resp.status_code)
    # print the json response
    print(resp.json())
    return resp.json()


def write_json(new_data, filename):
    with open(filename, 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["inventory"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)




# Create the receiver API POST endpoint:
@app.route("/inventory", methods=['GET'])
def getME():
    print("get from client")
    indata = request.data
    print(indata)
    print(type(indata))

    data = get_json()

    # Iterating through the json
    # list
    print("data ",data)
    # python object to be appended

    l = []
    for e in data:
        print("e: ",e)
        l.append({"id": e['id'], "benefit_cost": round(int(e['benefit'])/int(e['cost']), 2)})

    print(l)
    outdata={'metric': l}
    print(outdata)

    return outdata

if __name__ == "__main__":
    app.run(debug=True)

print("hallo")
