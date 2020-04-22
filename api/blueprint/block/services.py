"""Service layer for the block blueprint.
"""
from api.blueprint.block import sql, util
from api.blueprint.block.schema import BlockSchema
from api.database import db
from api.error.definition import ResourceNotFound


def retrieve_block(block_id):
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

    # target and difficulty are tricky to derive from nbits so we do it here instead of in the query
    # the value is the hexadecimal representation of the target with the leading 0x.
    target = util.compute_target(data["nbits"])
    pdiff = util.compute_pdiff(target)
    bdiff = util.compute_bdiff(target)
    data.update({"target": f"{target}:#066x", "pdifficulty": pdiff, "bdifficulty": bdiff})

    return BlockSchema(data)
