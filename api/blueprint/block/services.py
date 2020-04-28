"""Service layer for the block blueprint.
"""
from jsonschema import Draft7Validator

from api.blueprint.block import sql, util
from api.config import version
from api.database import db
from api.error.definition import ResourceNotFound
from api.resource import ApiResource
from api.schema import store


def retrieve(block_hash: str) -> dict:
    """Retrieve a block.
    
    :param block_hash: the hash of the block to retrieve.
    :returns: the query result.
    """
    result = None
    with db.cursor() as cursor:
        cursor.execute(sql.RETRIEVE, {"hash": bytearray.fromhex(block_hash)})
        result = cursor.fetchone()
    if result is None:
        raise ResourceNotFound(ApiResource.BLOCK, block_hash, parameter="id")

    return _to_api_types(dict(result))


def create(**kwargs) -> dict:
    """Create a block.

    :returns: the created block data.
    """
    validator = Draft7Validator(store.block)
    validator.validate(kwargs)

    params = _to_database_types({k: v for k, v in kwargs.items()})
    with db.cursor() as cursor:
        cursor.execute(sql.CREATE, params)
        data = dict(cursor.fetchone())
    return _to_api_types(data)


def delete(block_hash: str) -> dict:
    """Delete a block.

    :param block_hash: the hash of the block to delete.
    :returns: the deletion message.
    """
    with db.cursor() as cursor:
        cursor.execute(sql.DELETE, {"hash": bytearray.fromhex(block_hash)})
    return {"object": ApiResource.BLOCK, "hash": block_hash, "deleted": True}


def list_(limit=None, after=None, before=None) -> dict:
    """List blocks.
    """
    result = None
    with db.cursor() as cursor:
        cursor.execute(sql.LIST, {"limit": int(limit)})
        result = cursor.fetchall()
    if result is None:
        return {
            "object": ApiResource.LIST,
            "has_more": False,
            "count": 0,
            "data": [],
            "api_version": version.API_VERSION,
        }
    return _to_list_result(result)


def _add_target_information(data: dict) -> dict:
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


def _to_database_types(data: dict) -> dict:
    """Convert values in the dictionary to the relevant database type for insert.
    Note: this function alters its parameter, it is not pure.

    :param data: the data to insert. The data must come from a validated block json schema.
    :returns: a modified dictionary with the data ready to be inserted.
    """
    data["nbits"] = data["nbits"].to_bytes(4, byteorder="little", signed=False)
    data["hash"] = bytearray.fromhex(data["hash"])
    data["merkle_root"] = bytearray.fromhex(data["merkle_root"])
    data["previous_hash"] = bytearray.fromhex(data["previous_hash"])
    return data


def _to_api_types(data: dict) -> dict:
    """Convert values coming from a database query into the relevant type for api consumers.
    Note: this function alters its parameter, it is not pure.
    This is roughly the opposite of _to_database_types except that the data is enriched with computed, read-only values.
    
    :param data: the data coming from the database query. The data must conform to the block json schema.
    :returns: a modified dictionary with the data ready to be returned by the api.
    """
    data = _add_target_information(data)
    data["nbits"] = int.from_bytes(data["nbits"], byteorder="little", signed=False)
    data["hash"] = data["hash"].hex()
    data["merkle_root"] = data["merkle_root"].hex()
    data["previous_hash"] = data["previous_hash"].hex()
    data["api_version"] = version.API_VERSION
    data["object"] = ApiResource.BLOCK
    data["created_at"] = int(data["created_at"].timestamp())
    return data


def _to_list_result(data: list) -> dict:
    """Convert values coming from a list query on the database into the relevant list wrapper object for api consumers.
    
    :param data: the data coming from the database query. With the exception of the list specific fields, each item in the data must
    conform to the block json schema. List specific fields are `count` and `has_more`.
    :returns: a list wrapper object as a dictionary with the data ready to be returned by the api.
    """
    count = 0
    has_more = False
    blocks = list()
    for r in data:
        block_data = _to_api_types(dict(r))
        block_data.pop("count")
        block_data.pop("has_more")
        blocks.append(block_data)
    return {
        "object": ApiResource.LIST,
        "has_more": has_more,
        "count": count,
        "data": blocks,
        "api_version": version.API_VERSION,
    }
