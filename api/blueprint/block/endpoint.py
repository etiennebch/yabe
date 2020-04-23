"""Endpoints for the block blueprint.
"""
from http import HTTPStatus

from flask import jsonify, request

from api.blueprint.block import services
from api.decorators import listable


def retrieve(block_id):
    """Retrieve a specific block id.
    """
    block_data = services.retrieve(block_id)
    return (jsonify(block_data), HTTPStatus.OK)


def create():
    """Create a block.
    """
    block_data = services.create(**request.json)
    return (jsonify(block_data), HTTPStatus.CREATED)


@listable
def list(pagination):
    """List blocks.
    """
    list_data = services.list(**pagination)
    return (jsonify(list_data), HTTPStatus.OK)
