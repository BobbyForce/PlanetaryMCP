# This file needs to have view functions which grab the data necessary for
# the different types of prompts the AI may be asked.
# We also need to handle storing user interaction in Redis
from flask import Flask, jsonify, request

from functools import wraps
import time
import json
from typing import Callable, ParamSpec, TypeVar
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


P = ParamSpec("P")
R = TypeVar("R")


def track_query_count(view_function: Callable[P, R]) -> Callable[P, R]:
    @wraps(view_function)
    def wrapped(*args: P.args, **kwargs: P.kwargs) -> R:
        redis_conn.incr("query_count")
        return view_function(*args, **kwargs)

    return wrapped

@app.route("/guides", methods=["GET"])
@track_query_count
def get_planets():
    planets = mongo_conn["sample_guides"]["planets"].find({}, {"_id": 0})
    return jsonify(list(planets))


@app.route("/guides/atmosphere/h2", methods=["GET"])
@track_query_count
def get_planets_with_h2():
    return get_planets_by_gas("H2")


def get_planets_by_gas(gas: str):
    planets = mongo_conn["sample_guides"]["planets"].find(
        {"mainAtmosphere": gas},
        {"_id": 0, "name": 1, "mainAtmosphere": 1},
    )
    return jsonify(list(planets))


@app.route("/guides/atmosphere", methods=["GET"])
@track_query_count
def get_planets_with_atmosphere():
    gas = request.args.get("gas", "").strip()
    if not gas:
        return jsonify({"error": "The 'gas' query parameter is required."}), 400
    return get_planets_by_gas(gas)


@app.route("/guides/order", methods=["GET"])
@track_query_count
def get_planets_by_order():
    planets = mongo_conn["sample_guides"]["planets"].find(
        {},
        {"_id": 0, "name": 1, "orderFromSun": 1},
    ).sort("orderFromSun", 1)
    return jsonify(list(planets))


@app.route("/guides/temperature/ranked", methods=["GET"])
@track_query_count
def get_planets_by_mean_temperature():
    planets = mongo_conn["sample_guides"]["planets"].find(
        {"surfaceTemperatureC.mean": {"$type": "number"}},
        {"_id": 0, "name": 1, "orderFromSun": 1, "surfaceTemperatureC.mean": 1},
    ).sort("surfaceTemperatureC.mean", -1)
    return jsonify(list(planets))


@app.route("/guides/temperature-distance", methods=["GET"])
@track_query_count
def get_planet_temperatures_by_order():
    planets = mongo_conn["sample_guides"]["planets"].find(
        {},
        {"_id": 0, "name": 1, "orderFromSun": 1, "surfaceTemperatureC.mean": 1},
    )
    return jsonify(list(planets))


@app.route("/guides/rings", methods=["GET"])
@track_query_count
def get_planet_ring_status():
    planets = mongo_conn["sample_guides"]["planets"].find(
        {},
        {"_id": 0, "name": 1, "hasRings": 1},
    )
    return jsonify(list(planets))

@app.route("/stats", methods=["GET"])
def get_stat():
    key = request.args.get("key", "")
    value = redis_conn.get(key)
    return jsonify({"key": key, "value": value.decode() if value else None})
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8051)
