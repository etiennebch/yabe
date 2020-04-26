"""Routing rules for the block blueprint.
The block blueprint exposes endpoints about individual blocks on the blockchain.
"""
from flask import Blueprint

from api.blueprint.block import endpoint

block = Blueprint("block", __name__, url_prefix="/blocks")

block.add_url_rule("/<string:block_hash>", endpoint="retrieve", methods=["GET"], view_func=endpoint.retrieve)
block.add_url_rule("", endpoint="create", methods=["POST"], view_func=endpoint.create)
block.add_url_rule("/<string:block_hash>", endpoint="delete", methods=["DELETE"], view_func=endpoint.delete)
