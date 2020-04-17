"""Service layer for the block blueprint.
"""
from api.blueprint.block import sql, util
from api.blueprint.block.schema import BlockSchema
from api.blueprint.error.definition import NotFound
from api.extension import db


def retrieve_block(block_id):
    """Retrieve a block.
    
    :param block_id: the id of the block to retrieve.
    :type block_id: integer.
    :returns: the query result as a marshmallow schema.
    :rtype: BlockSchema.
    """
    result = db.session.execute(sql.RETRIEVE, {"id": block_id}).fetchone()
    if result is None:
        raise NotFound(BlockSchema.object_name(), block_id, parameter="id")

    # target and difficulty are tricky to derive from nbits so we do it here instead of in the query
    # the value is the hexadecimal representation of the target with the leading 0x.
    target = util.compute_target(result["nbits"])
    pdiff = util.compute_pdiff(target)
    bdiff = util.compute_bdiff(target)
    result.update({"target": f"{target}:#066x", "pdifficulty": pdiff, "bdifficulty": bdiff})

    return BlockSchema(dict(result))
