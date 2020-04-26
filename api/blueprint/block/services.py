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

    data = dict(result)
    data = _add_target_information(data)
    data["nbits"] = int.from_bytes(data["nbits"], byteorder="little", signed=False)
    data["hash"] = data["hash"].hex()
    data["merkle_root"] = data["merkle_root"].hex()
    data["previous_hash"] = data["previous_hash"].hex()
    data["api_version"] = version.API_VERSION
    data["object"] = ApiResource.BLOCK.value
    data["created_at"] = int(data["created_at"].timestamp())
    return data


# TODO parameter formatting should be handled in separate functions
def create(**kwargs):
    """Create a block.
    """
    validator = Draft7Validator(store.block)
    validator.validate(kwargs)

    params = {k: v for k, v in kwargs.items()}
    params["nbits"] = params["nbits"].to_bytes(4, byteorder="little", signed=False)
    params["hash"] = bytearray.fromhex(params["hash"])
    params["merkle_root"] = bytearray.fromhex(params["merkle_root"])
    params["previous_hash"] = bytearray.fromhex(params["previous_hash"])

    with db.cursor() as cursor:
        cursor.execute(sql.CREATE, params)
        data = dict(cursor.fetchone())

    data = _add_target_information(data)
    data["nbits"] = int.from_bytes(data["nbits"], byteorder="little", signed=False)
    data["hash"] = data["hash"].hex()
    data["merkle_root"] = data["merkle_root"].hex()
    data["previous_hash"] = data["previous_hash"].hex()
    data["api_version"] = version.API_VERSION
    data["object"] = ApiResource.BLOCK.value
    data["created_at"] = int(data["created_at"].timestamp())
    return data


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
