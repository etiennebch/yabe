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

    params = _to_database_types(kwargs)
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
        cursor.execute(sql.LIST, {"limit": limit, "after": after, "before": before})
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


def _get_difficulty(nbits: bytes) -> dict:
    """Compute and return difficulty information.
    
    :param nbits: the nbits data as returned by a create, retrieve or list query.
    :returns: the difficulty information.
    """
    # the value is the hexadecimal representation of the target with the leading 0x.
    target = util.compute_target(nbits)
    pdiff = util.compute_pdiff(target)
    bdiff = util.compute_bdiff(target)
    return {
        "target": f"{target:#066x}",
        "pdifficulty": str(pdiff),
        "bdifficulty": str(bdiff),
        "nbits": int.from_bytes(nbits, byteorder="little", signed=False),
    }


def _to_database_types(data: dict) -> dict:
    """Convert values in the dictionary to the relevant database types for insert.
    This function essentially maps the json schema to insert parameters.

    :param data: the data to insert. The data must come from a validated block json schema.
    :returns: a dictionary with the data ready to be accepted to parametrize an insert query.
    """
    params = data
    params["hash"] = bytearray.fromhex(params["hash"])
    params["nbits"] = params["difficulty"]["nbits"].to_bytes(4, byteorder="little", signed=False)
    params["merkle_root"] = bytearray.fromhex(data["merkle_root"])
    params["previous_hash"] = bytearray.fromhex(data["previous_hash"])
    params.pop("difficulty")
    return params


def _to_api_types(data: dict) -> dict:
    """Convert values coming from a database query into the relevant types for api consumers.
    This is roughly the opposite of _to_database_types except that the data is enriched with computed, read-only values.
    
    :param data: the data coming from the database query. The data must conform to the block json schema.
    :returns: a dictionary with the data ready to be returned by the api.
    """
    result = data
    result["difficulty"] = _get_difficulty(result.pop("nbits"))
    result["hash"] = result["hash"].hex()
    result["merkle_root"] = result["merkle_root"].hex()
    result["previous_hash"] = result["previous_hash"].hex()
    result["api_version"] = version.API_VERSION
    result["object"] = ApiResource.BLOCK
    result["created_at"] = int(result["created_at"].timestamp())
    return result


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
