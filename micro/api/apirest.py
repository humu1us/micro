from flask import jsonify
from flask import request
from flask import Blueprint
from .endpoints import _help
from .endpoints import _info
from .endpoints import _plugins
from .endpoints import _run

endpoints = Blueprint("endpoints", __name__)


@endpoints.route("/plugins", methods=["GET"])
def plugins():
    return jsonify(_plugins())


@endpoints.route("/info/<name>", methods=["GET"])
def info(name):
    return jsonify(_info(name))


@endpoints.route("/help/<name>", methods=["GET"])
def help(name):
    return jsonify(_help(name))


@endpoints.route("/run/<name>", methods=["POST"])
def run(name):
    kwargs = request.get_json()
    return jsonify(_run(name, **kwargs))
