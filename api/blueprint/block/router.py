"""Routing rules for the block blueprint.
The block blueprint exposes endpoints about individual blocks on the blockchain.
"""
from flask import Blueprint

from api.blueprint.block import endpoint

block = Blueprint("block", __name__, url_prefix="/blocks")

block.add_url_rule("/<int:block_id>", endpoint="retrieve", methods=["GET"], view_func=endpoint.retrieve)
