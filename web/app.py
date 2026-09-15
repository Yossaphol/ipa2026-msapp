import os
from bson import ObjectId
from flask import Flask, redirect, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

mongo_uri = os.environ.get("MONGO_URI")
db_name = os.environ.get("DB_NAME")

client = MongoClient(mongo_uri)
db = client[db_name or "routerdb"]
routers = db["routers"]
interface_status = db["interface_status"]


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", routers=list(routers.find()))


@app.route("/add", methods=["POST"])
def add_router():
    ip = request.form.get("ip")
    username = request.form.get("username")
    password = request.form.get("password")

    if ip and username and password:
        routers.insert_one({"ip": ip, "username": username, "password": password})
    return redirect("/")


@app.route("/delete/<id>", methods=["POST"])
def delete_router(id):
    routers.delete_one({"_id": ObjectId(id)})
    return redirect("/")


@app.route("/router/<router_ip>", methods=["GET"])
def router_detail(router_ip):
    logs = list(
        interface_status.find({"router_ip": router_ip}).sort("timestamp", -1).limit(5)
    )
    return render_template("router_detail.html", router_ip=router_ip, logs=logs)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
