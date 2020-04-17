"""Endpoints for the block blueprint.
"""
from flask import jsonify

from api.blueprint.block.services import retrieve_block


def retrieve(block_id):
    """Retrieve a specific block id.
    """
    block_data = retrieve_block(block_id)
    return (jsonify(block_data), 200)
