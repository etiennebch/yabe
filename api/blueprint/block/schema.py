"""Marshmallow schema for the block blueprint.
"""
from marshmallow import Schema

from api.serialization import field, schema


class InnerBlockSchema(Schema):
    """The schema for the JSON representation of block data.
    """

    hash_ = field.BinaryHexString(
        data_key="hash", attribute="hash", required=True, description="Hash of the block."
    )
    size = field.Integer(strict=True, required=True, description="Size of the block in bytes.")
    transaction_count = field.Integer(
        strict=True, required=True, description="Number of transactions included in the block."
    )
    version = field.Integer(strict=True, required=True, description="Block version number.")
    previous_hash = field.BinaryHexString(
        required=True, description="Hash of the previous block in the blockchain."
    )
    merkle_root = field.BinaryHexString(required=True, description="Root hash of the block's merkle tree.")
    timestamp = field.Integer(
        strict=True,
        required=True,
        description="Unix timestamp when the miner started hashing the header, according to the miner's clock.",
    )
    nbits = field.UInt32LE(required=True, description="The compact form of the difficulty.",)
    target = field.String(
        required=True,
        dump_only=True,
        description="Target threshold below which the block header hash must be, in hash form.",
    )
    pdifficulty = field.Decimal(
        as_string=True,
        dump_only=True,
        description="The pool difficulty computed as the ratio between the non truncated genesis target and the block target.",
    )
    bdifficulty = field.Decimal(
        as_string=True,
        dump_only=True,
        description="The approximate difficulty computed as the ratio between the truncated genesis target and the block target.",
    )
    nonce = field.Integer(
        strict=True, required=True, description="The value miners change to solve the proof of work.",
    )
    height = field.Integer(strict=True, required=True, description="Distance to the genesis block.")
    subsidy = field.Integer(
        strict=True, required=True, description="The amount in satoshis that mining the block releases.",
    )
    input_ = field.Integer(
        data_key="input",
        attribute="input",
        strict=True,
        required=True,
        description="The sum of the block's transactions inputs in satoshis.",
    )
    output = field.Integer(
        strict=True, required=True, description="The sum of the block's transactions outputs in satoshis.",
    )
    transaction_fee = field.Integer(
        strict=True, required=True, description="The difference between the input and the output in satoshis."
    )
    confirmations = field.Integer(
        strict=True, dump_only=True, description="Distance to the tip of the blockchain."
    )


class BlockSchema(schema.ResourceMixin):
    """The schema for the JSON representation of a block resource.
    """

    @staticmethod
    def object_name():
        return "block"

    data = field.Nested(InnerBlockSchema)
