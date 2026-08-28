from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from pymongo import MongoClient

app = Flask(__name__)

data = []

client = MongoClient("mongodb://mongo:27017/")
mydb = client["routerdb"]
mycol = mydb["routers"]

@app.route("/")
def main():
    data = list(mycol.find())
    return render_template("index.html", data=data)

@app.route("/add", methods=["POST"])
def add_comment():
    ip = request.form.get("ip")
    username = request.form.get("username")
    password = request.form.get("password")

    if ip and username and password:
        data.append({"ip": ip, "username": username})
        mycol.insert_one({
            "ip": ip,
            "username": username,
            "password": password
        })
    return redirect(url_for("main"))

@app.route("/delete", methods=["POST"])
def delete_comment():
    try:
        idx = int(request.form.get("idx"))
        data = list(mycol.find())
        if 0 <= idx < len(data):
            data.pop(idx)
            mycol.delete_one({"_id": data[idx]["_id"]})
    except Exception:
        pass
    return redirect(url_for("main"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)