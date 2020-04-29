"""Define the block data structure.
"""
from __future__ import annotations


class Block:
    """Represent a block.
    """

    # TODO: use proper block header class
    def __init__(self, version, prev_block, merkle_root, timestamp, bits, nonce, payload):
        """Constructor.
        """
        self.version = version
        self.prev_block = prev_block
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.bits = bits
        self.nonce = nonce
        self.payload = payload

    @staticmethod
    def deserialize(data: bytes) -> Block:
        """Deserialize block data.

        https://en.bitcoin.it/wiki/Protocol_documentation#Block_Headers

        :param data: the raw bytes to deserialize.
        """
        header = data[:80]
        payload = data[81:]
        version = int.from_bytes(header[:4], byteorder="little")
        prev_block = header[4:36]
        merkle_root = header[36:68]
        timestamp = int.from_bytes(header[-12:-8], byteorder="little")
        bits = int.from_bytes(header[-8:-4], byteorder="little")
        nonce = int.from_bytes(header[-4:], byteorder="little")
        block = Block(version, prev_block, merkle_root, timestamp, bits, nonce, payload)
        return block
