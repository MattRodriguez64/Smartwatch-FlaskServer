from flask import Flask, render_template, url_for, request, redirect
from random import randint
import requests
import json

data_url = "http://localhost:8080/smartwatch/api/datas"
url = "http://localhost:8080/smartwatch/api/auth"
headers = {
    'Content-type': 'application/json',
    'User-Agent': 'XY'
}

app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        loginUser = request.form["login"]
        passwordUser = request.form["password"]

        payload = json.dumps({
            "login": loginUser,
            "password": passwordUser
        })

        response = requests.request("POST", url, data=payload, headers=headers)
        token = response.text
        headers['Authorization'] = f"Bearer {token}"

        print(response.text)
        print(headers)

        currentId = randint(1, 5)

        return redirect(url_for("infos", id=currentId))
    return render_template("index.html")


@app.route('/infos/<int:id>')
def infos(id: int):
    allUserDatas = requests.get(f"{data_url}/_search/?userId={id}", headers=headers)
    print(allUserDatas.json())

    allPas = [elt['pas'] for elt in allUserDatas.json()]
    allNumber = [i for i in range(0, len(allPas))]
    print(allNumber)

    allCalories = [elt['calorie'] for elt in allUserDatas.json()]
    allTensions = [elt['tension'] for elt in allUserDatas.json()]
    allRythmes = [elt['rythmeCardiaque'] for elt in allUserDatas.json()]

    #Sommeil
    allSommeil = [elt['sommeil'] for elt in allUserDatas.json()]
    allSommeilTraitement = []
    for elt in allSommeil:
        elt.replace("min", "")
        heure = int(elt.split("h")[0])
        minute = int(elt.split("h")[1].replace("min", ""))
        #print(f"{elt} - Heure : {heure} - Minute : {minute}")
        allSommeilTraitement.append(int(minute + (heure * 60)))

    #print(allSommeilTraitement)

    return render_template("data.html",
                           allUserDatas=allUserDatas.json(),
                           allPas=allPas,
                           allNumber=allNumber,
                           allCalories=allCalories,
                           allTensions=allTensions,
                           allRythmes=allRythmes,
                           allSommeil=allSommeilTraitement
                           )


if __name__ == "__main__":
    app.run(debug=True)
