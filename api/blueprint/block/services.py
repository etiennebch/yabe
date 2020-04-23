"""Service layer for the block blueprint.
"""
from api.blueprint.block import sql, util
from api.blueprint.block.schema import BlockSchema, InnerBlockSchema
from api.database import db
from api.error.definition import ResourceNotFound


def retrieve(block_id):
    """Retrieve a block.
    
    :param block_id: the id of the block to retrieve.
    :type block_id: integer.
    :returns: the query result as a marshmallow schema.
    :rtype: BlockSchema.
    """
    result = db.cursor.execute(sql.RETRIEVE, {"id": block_id})
    if result is None:
        raise ResourceNotFound(BlockSchema.object_name(), block_id, parameter="id")

    data = result.fetchone()
    data = _add_target_information(data)

    schema = BlockSchema()
    return schema.dump({"id": block_id, "created_at": data.pop("created_at"), "data": data})


def create(**kwargs):
    """Create a block.
    """
    schema = InnerBlockSchema()
    params = schema.load(kwargs)
    data = None
    with db.cursor() as cursor:
        cursor.execute(sql.CREATE, params)
        data = dict(cursor.fetchone())
    data = _add_target_information(data)
    return schema.dump(data)


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
    data.update({"target": f"{target:#066x}", "pdifficulty": pdiff, "bdifficulty": bdiff})
    return data
