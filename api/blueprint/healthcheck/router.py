"""Routing rules for the healthcheck blueprint.
The healthcheck blueprint exposes endpoints to inquire about the overall status of the api.
"""
from flask import Blueprint

from api.blueprint.healthcheck import endpoint

healthcheck = Blueprint("healthcheck", __name__, url_prefix="/")

healthcheck.add_url_rule("", methods=["GET"], view_func=endpoint.ping)
