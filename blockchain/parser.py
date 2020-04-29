"""Define methods to parse the raw blockchain data, as dumped into blk*.dat files.
https://en.bitcoin.it/wiki/Bitcoin_Core_0.11_(ch_2):_Data_Storage#Raw_Block_data_.28blk.2A.dat.29
https://learnmeabitcoin.com/guide/blkdat

Blocks are dumped to disk **almost** as received by the network. The protocol documents the structure
of a message, which is needed to parse the blk*.dat files.
https://github.com/bitcoin/bitcoin/blob/master/src/protocol.h

https://en.bitcoin.it/wiki/Protocol_documentation#Message_structure
NB: Data is almost always written as little endian.
The structure of a message header is:
- 4 bytes: message start (magic number)
- 12 bytes: command
- 4 bytes: size of the message
- 4 bytes: checksum

However, only the magic number, size and serialized block data is written to disk.
This can be seen in the function WriteBlockToDisk: https://github.com/bitcoin/bitcoin/blob/master/src/validation.cpp
The function writes an **index header** which consists of the message start and the size

"""
from typing import BinaryIO, Generator

# the size in bytes of sections of the message header
MESSAGE_START = 4
MESSAGE_COMMAND = 12
MESSAGE_SIZE = 4
MESSAGE_CHECKSUM = 4


def read(file_: BinaryIO) -> Generator[bytes, None, None]:
    """Read the file at filename and parses it according to the block structure definition.
    :returns: a generator yielding serialized block data.
    """
    offset = MESSAGE_START + MESSAGE_SIZE
    header = file_.read(offset)
    size = int.from_bytes(header[MESSAGE_START:], byteorder="little", signed=True)
    yield file_.read(size)
