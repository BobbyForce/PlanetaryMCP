from flask import Flask, jsonify

import time
import json
from db_config import get_redis_connection, get_mongo_connection
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(
    app,
    version="1.0",
    title="Flask App using Mongo/Redis",
    description="A simple API to demonstrate the power of RestAPI using Redis and Mongo",
)

# Establish database connections
redis_conn = get_redis_connection()
mongo_conn = get_mongo_connection()

@api.route("/", methods=["GET"])
def get_homescreen():
    return None


@api.route("/guides", methods=["GET"])
def get_planets():
    return None


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
