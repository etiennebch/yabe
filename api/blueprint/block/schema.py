"""Marshmallow schema for the block blueprint.
"""
from marshmallow import fields

from api import serialization


class BlockSchema(serialization.ResourceMixin):
    """The schema for the JSON representation of a block resource.
    """

    @staticmethod
    def object_name():
        return "block"

    hash_ = fields.String(data_key="hash", required=True, description="Hash of the block.")
    size = fields.Integer(strict=True, required=True, description="Size of the block in bytes.")
    transaction_count = fields.Integer(
        strict=True, required=True, description="Number of transactions included in the block."
    )
    version = fields.Integer(as_string=True, required=True, description="Block version number.")
    previous_hash = fields.String(required=True, description="Hash of the previous block in the blockchain.")
    merkle_root = fields.String(required=True, description="Root hash of the block's merkle tree.")
    timestamp = fields.Integer(
        strict=True,
        as_string=True,
        required=True,
        description="Unix timestamp when the miner started hashing the header, according to the miner's clock.",
    )
    nbits = fields.Integer(
        strict=True,
        required=True,
        description="Compact format of the target threshold below which the block header hash must be.",
    )
    target = fields.String(
        required=True,
        description="Target threshold below which the block header hash must be, in hash form.",
    )
    nonce = fields.Integer(
        strict=True, required=True, description="The value miners change to solve the proof of work.",
    )
    height = fields.Integer(strict=True, required=True, description="Distance to the genesis block.")
    subsidy = fields.Integer(
        strict=True, required=True, description="The amount in satoshis that mining the block releases.",
    )
    input_ = fields.Integer(
        data_key="input",
        strict=True,
        required=True,
        description="The sum of the block's transactions inputs in satoshis.",
    )
    output = fields.Integer(
        strict=True, required=True, description="The sum of the block's transactions outputs in satoshis.",
    )
    transaction_fee = fields.Integer(
        dump_only=True, description="The difference between the input and the output in satoshis."
    )
    confirmations = fields.Integer(
        strict=True, dump_only=True, description="Distance to the tip of the blockchain."
    )
