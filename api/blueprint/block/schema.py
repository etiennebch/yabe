"""Marshmallow schema for the block blueprint.
"""
from marshmallow import Schema, fields

from api import serialization


class BlockSchema(Schema):
    """The schema for the JSON representation of a block resource.
    """

    id_ = serialization.Identifier()
    hash_ = fields.String(data_key="hash", description="The hash of the block.")
    size = fields.Integer(strict=True, description="The size of the block in bytes.")
    transaction_count = fields.Integer(strict=True, description="The number of transactions included in the block.")
    version = fields.Integer(as_string=True, description="The block version number.")
    previous_hash = fields.String(description="The hash of the previous block in the blockchain.")
    merkle_root = fields.String(description="The root hash of the block's merkle tree.")
    timestamp = fields.Integer(
        strict=True,
        as_string=True,
        description="The unix timestamp when the miner started hashing the header, according to the miner's clock.",
    )
    nbits = fields.Integer(
        strict=True,
        description="The compact format of the target threshold below which the block header hash must be.",
    )
    target = fields.String(description="The target threshold below which the block header hash must be in hash form.")
    nonce = fields.Integer(strict=True, description="The value miners change to solve the proof of work.")
    height = fields.Integer(strict=True, description="The distance to the genesis block.")
    subsidy = fields.Integer(strict=True, description="The amount in satoshis that mining the block releases.")
    input_ = fields.Integer(
        data_key="input", strict=True, description="The sum of the block's transactions inputs in satoshis."
    )
    output = fields.Integer(strict=True, description="The sum of the block's transactions outputs in satoshis.")
    transaction_fee = fields.Integer(
        dump_only=True, description="The difference between the input and the output in satoshis."
    )
