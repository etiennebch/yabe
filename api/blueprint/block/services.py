"""Service layer for the block blueprint.
"""
from jsonschema import Draft7Validator

from api.blueprint.block import sql, util
from api.config import version
from api.database import db
from api.error.definition import ResourceNotFound
from api.resource import ApiResource
from api.schema import store


def retrieve(block_hash):
    """Retrieve a block.
    
    :param block_hash: the hash of the block to retrieve.
    :type block_id: string.
    :returns: the query result.
    :rtype: dict.
    """
    result = None
    with db.cursor() as cursor:
        cursor.execute(sql.RETRIEVE, {"hash": bytearray.fromhex(block_hash)})
        result = cursor.fetchone()
    if result is None:
        raise ResourceNotFound(ApiResource.BLOCK, block_hash, parameter="id")

    return _to_api_types(dict(result))


def create(**kwargs):
    """Create a block.
    """
    validator = Draft7Validator(store.block)
    validator.validate(kwargs)

    params = _to_database_types({k: v for k, v in kwargs.items()})
    with db.cursor() as cursor:
        cursor.execute(sql.CREATE, params)
        data = dict(cursor.fetchone())
    return _to_api_types(data)


def delete(block_hash):
    """Delete a block.

    :param block_hash: the hash of the block to delete.
    :type block_id: string.
    :returns: the deletion message.
    :rtype: dict.
    """
    with db.cursor() as cursor:
        cursor.execute(sql.DELETE, {"hash": bytearray.fromhex(block_hash)})
    return {"object": ApiResource.BLOCK.value, "hash": block_hash, "deleted": True}


def list(**kwargs):
    """List blocks.
    """
    raise NotImplementedError()


def _add_target_information(data):
    """Compute and add target information to block data returned by the database.
    Target and difficulty are tricky to derive from nbits so we do it here instead of in the query
    
    :param data: the block data as returned by a create or retrieve query.
    :type data: dict.
    :returns: the updated data.
    :rtype: dict.
    """
    # the value is the hexadecimal representation of the target with the leading 0x.
    target = util.compute_target(data["nbits"])
    pdiff = util.compute_pdiff(target)
    bdiff = util.compute_bdiff(target)
    data.update({"target": f"{target:#066x}", "pdifficulty": str(pdiff), "bdifficulty": str(bdiff)})
    return data


def _to_database_types(data):
    """Convert values in the dictionary to the relevant database type for insert.
    Note: this function alters its parameter, it is not pure.

    :param data: the data to insert. The data must come from a validated block json schema.
    :type data: dict.
    :returns: a modified dictionary with the data ready to be inserted.
    :rtype: dict.
    """
    data["nbits"] = data["nbits"].to_bytes(4, byteorder="little", signed=False)
    data["hash"] = bytearray.fromhex(data["hash"])
    data["merkle_root"] = bytearray.fromhex(data["merkle_root"])
    data["previous_hash"] = bytearray.fromhex(data["previous_hash"])
    return data


def _to_api_types(data):
    """Convert values coming from a database query into the relevant type for api consumers.
    Note: this function alters its parameter, it is not pure.
    This is roughly the opposite of _to_database_types except that the data is enriched with computed, read-only values.
    
    :param data: the data coming from the database query. The data must conform to the block json schema.
    :type data: dict.
    :returns: a modified dictionary with the data ready to be returned by the api.
    :rtype: dict.
    """
    data = _add_target_information(data)
    data["nbits"] = int.from_bytes(data["nbits"], byteorder="little", signed=False)
    data["hash"] = data["hash"].hex()
    data["merkle_root"] = data["merkle_root"].hex()
    data["previous_hash"] = data["previous_hash"].hex()
    data["api_version"] = version.API_VERSION
    data["object"] = ApiResource.BLOCK.value
    data["created_at"] = int(data["created_at"].timestamp())
    return data
