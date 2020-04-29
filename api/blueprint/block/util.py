"""Helpers for the block blueprint.
"""
import decimal

GENESIS_TARGET = decimal.Decimal(
    int("0x00000000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF", 16)
)
GENESIS_TARGET_TRUNCATED = decimal.Decimal(
    int("0x00000000FFFF0000000000000000000000000000000000000000000000000000", 16)
)


def compute_target(nbits: bytes) -> int:
    """Derive the target from the difficulty compact form stored with the block.
    
    https://en.bitcoin.it/wiki/Difficulty#How_is_difficulty_stored_in_blocks.3F
    
    From https://github.com/bitcoin/bitcoin/blob/master/src/arith_uint256.h#L250

    * The "compact" format is a representation of a whole
    * number N using an unsigned 32bit number similar to a
    * floating point format.
    * The most significant 8 bits are the unsigned exponent of base 256.
    * This exponent can be thought of as "number of bytes of N".
    * The lower 23 bits are the mantissa.
    * Bit number 24 (0x800000) represents the sign of N.
    * N = (-1^sign) * mantissa * 256^(exponent-3)
    *
    * Satoshi's original implementation used BN_bn2mpi() and BN_mpi2bn().
    * MPI uses the most significant bit of the first byte as sign.
    * Thus 0x1234560000 is compact (0x05123456)
    * and  0xc0de000000 is compact (0x0600c0de)
    *
    * Bitcoin only uses this "compact" format for encoding difficulty
    * targets, which are unsigned 256bit quantities.  Thus, all the
    * complexities of the sign bit and using base 256 are probably an
    * implementation accident.

    :param nbits: the difficulty of the block in the compact form. nbit is assumed to be ordered little endian and can be
    represented as a uint32 integer (4 bytes).
    :returns: the target of the block.
    """
    exponent = int.from_bytes(nbits[-1], byteorder="little", signed=False)
    mantissa = int.from_bytes(nbits[:-1], byteorder="little", signed=False)
    # since targets are never negative in practice, we don't care about the sign.
    # https://en.bitcoin.it/wiki/Difficulty#How_is_difficulty_stored_in_blocks.3F
    # N = mantissa * 256(exponent -3)
    return mantissa * 256 ** (exponent - 3)


def compute_pdiff(target):
    """Compute the p-difficulty as given by the ratio between the non truncated genesis block target
    and the current target.

    https://en.bitcoin.it/wiki/Difficulty#How_is_difficulty_calculated.3F_What_is_the_difference_between_bdiff_and_pdiff.3F

    :param target: the current target.
    :type target: integer.
    """
    return GENESIS_TARGET / decimal.Decimal(target)


def compute_bdiff(target):
    """Compute the b-difficulty as given by the ration between the truncated genesis block target
    and the current target.
    
    https://en.bitcoin.it/wiki/Difficulty#How_is_difficulty_calculated.3F_What_is_the_difference_between_bdiff_and_pdiff.3F
    
    :param target: the current target.
    :type target: integer.
    """
    return GENESIS_TARGET_TRUNCATED / decimal.Decimal(target)
