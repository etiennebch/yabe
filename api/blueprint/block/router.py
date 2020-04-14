"""Routing rules for the block blueprint.
The block blueprint exposes endpoints about individual blocks on the blockchain.
"""
from flask import Blueprint

block = Blueprint("block", __name__, url_prefix="/block")
