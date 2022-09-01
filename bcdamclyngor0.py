from clyngor import ASP, solve
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from requests.structures import CaseInsensitiveDict

# <strong>#Set up Flaskstrong>:
app = Flask(__name__)
# <strong>#Set up Flask to bypass CORSstrong>:
cors = CORS(app)

debug = False


def printdebug(x):
    if debug:
        print(x)


def get_json_from_server():
    url = "http://localhost:3000/backlog"

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    resp = requests.get(url, headers=headers)
    print("xget_json: ", resp.status_code)
    # print the json response
    print(resp.json())
    return resp.json()


def write_lp_input(new_data, keyword, position, filename):
    print("Write: new data: ", new_data, "keyword: ", keyword, "position: ", position, "\n")

    # opening the file in read mode
    file = open(filename, "r")
    replacement = ""

    # using the for loop
    for line in file:

        line = line.strip()
        words = line.split()

        if len(words) > position and words[position] == keyword:
            print("words 1:", words[position])
            w = line
            changes = line.replace(w, new_data)
        else:
            changes = line
        replacement = replacement + changes + "\n"
        print("replacement: ", replacement)

    file.close()
    print("infile closed: ", "new data: ", new_data, "keyword: ", keyword, "position: ", position, "replacement: ",
          replacement, "\n")
    # opening the file in write mode
    fout = open(filename, "w")
    fout.write(replacement)
    fout.close()

    # Join new_data with file_data inside emp_details
    # file_data["inventory"].append(new_data)
    # Sets file's current position at offset.
    ##file.seek(0)
    # convert back to json.
    # json.dump(file_data, file, indent=4)


# Create the receiver API POST endpoint:
@app.route("/receiver", methods=["POST", "GET"])
def postME():
    data = request.get_json()
    print(data[0]['command'])
    print(type(data))

    print("get from client")
    xdata = get_json_from_server()

    print("xdata: ", xdata)
    # python object to be appended

    # Get epics from json format and make ASP string for epics
    epics = map(lambda e: e['epic'], xdata)
    epics = list(epics)
    print("epics: ", epics)
    epicsstring = '; '.join(epics)
    # by the way, write the init string using the preliminary epicssstring.
    inbacklogstring = 'init( inbacklog (' + epicsstring + ') ).'
    write_lp_input(inbacklogstring, 'inbacklog', 1, "bcdamgoaldriveninput.lp")

    # by the way, write the goal production string using the preliminary epicssstring.
    goalstring = 'goal( inproduction (' + epicsstring + ') ).'
    write_lp_input(goalstring, 'inproduction', 1, "bcdamgoaldriveninput.lp")
    epicsstring = 'epic (' + epicsstring + ').'
    print("epicsstring: ", epicsstring)
    write_lp_input(epicsstring, 'epic', 0, "bcdamgoaldriveninput.lp")

    # Get benefits from json format and make ASP string for benefits
    benefits = map(lambda e: e['benefit'], xdata)
    benefits = list(benefits)
    print("benefits: ", benefits)
    benefitsstring = '; '.join(benefits)
    # convert string to list of 'benefit;'
    benefits = list(benefitsstring.split(" "))
    print("benefits: ", benefits)
    # interleave epics list and benefits list
    epicsbenefits = [*sum(zip(epics, benefits), ())]
    print("epicsbenefits: ", epicsbenefits)
    # convert back to string
    epicsbenefitsstring = ', '.join(epicsbenefits)
    epicsbenefitsstring = 'benefit (' + epicsbenefitsstring + ').'
    print("epicsbenefitsstring: ", epicsbenefitsstring)
    # replace ;, with ;
    epicsbenefitsstring = epicsbenefitsstring.replace(';,', ';')
    print("epicsbenefitsstring: ", epicsbenefitsstring)
    write_lp_input(epicsbenefitsstring, 'benefit', 0, "bcdamgoaldriveninput.lp")

    # Get costs from json format and make ASP string for costs
    costs = map(lambda e: e['cost'], xdata)
    costs = list(costs)
    print("costs: ", costs)
    costsstring = '; '.join(costs)
    # convert string to list of 'cost;'
    costs = list(costsstring.split(" "))
    print("costs: ", costs)
    # interleave epics list and costs list
    epicscosts = [*sum(zip(epics, costs), ())]
    print("epicscosts: ", epicscosts)
    # convert back to string
    epicscostsstring = ', '.join(epicscosts)
    epicscostsstring = 'cost (' + epicscostsstring + ').'
    print("epicscostsstring: ", epicscostsstring)
    # replace ;, with ;
    epicscostsstring = epicscostsstring.replace(';,', ';')
    print("epicscostsstring: ", epicscostsstring)
    write_lp_input(epicscostsstring, 'cost', 0, "bcdamgoaldriveninput.lp")

    # Replicate cost to time until json data has time as well.
    epicstimestring = ', '.join(epicscosts)
    epicstimestring = 'time (' + epicstimestring + ').'
    epicstimestring = epicstimestring.replace(';,', ';')
    write_lp_input(epicstimestring, 'time', 0, "bcdamgoaldriveninput.lp")

    # epicsbenefitsstring = ";".join(i + j for i, j in zip(epicsstring, benefitsstring))

    answers = solve('bcdamgoaldriveninput.lp', 'bcdamgoaldriven.lp')
    print("holds in answer")

    i = 0

    for answer in answers.by_predicate:
        print("answer no: ", i)
        i = i + 1
        print(type(answer))
        print("answer: ", answer)
        holds_list = [list(x) for x in (answer['holds'])]
        print("holds_list: ", holds_list)
        holds_list_sorted = sorted(holds_list, key=lambda e: e[1])
        print("holds_list_sorted: ", holds_list_sorted)
        holds_list_sorted_json = list(map(lambda e: {"holds": e[0], "T": e[1]}, holds_list_sorted))
        print("holds_list_sorted_json: ", holds_list_sorted_json)

        benefitrealized_list = [list(x) for x in (answer['benefitrealized'])]
        print("benefitrealized_list: ", benefitrealized_list)
        benefitrealized_list_sorted = sorted(benefitrealized_list, key=lambda e: e[1])
        print("benefitrealized_list_sorted: ", benefitrealized_list_sorted)
        benefitrealized_list_sorted_json = list(map(lambda e: {"metric": e[0], "T": e[1]}, benefitrealized_list_sorted))
        print("benefitrealized_list_sorted_json: ", benefitrealized_list_sorted_json)

        costincurred_list = [list(x) for x in (answer['costincurred'])]
        costincurred_list_sorted = sorted(costincurred_list, key=lambda e: e[1])
        costincurred_list_sorted_json = list(map(lambda e: {"metric": e[0], "T": e[1]}, costincurred_list_sorted))
        metrics = [{'theme': 'predicates', 'data': holds_list_sorted_json},
                   {'theme': 'benefit', 'data': benefitrealized_list_sorted_json},
                   {'theme': 'cost', 'data': costincurred_list_sorted_json}]
        print(metrics)

    if (data[0]['command'] == 'holds'):
        data = jsonify(holds_list_sorted_json)
    else:
        # data = jsonify(benefitrealized_list_sorted_json)
        data = jsonify(metrics)
    print(data)
    return data


def getME():
    data = request.get_json()
    print(data[0])
    print(type(data))
    return data


if __name__ == "__main__":
    app.run(port=5001, debug=True)

print("hei")
