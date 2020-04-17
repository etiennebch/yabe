"""Service layer for the block blueprint.
"""
from api.blueprint.block import sql
from api.blueprint.block.schema import BlockSchema
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
        # TODO 404
        pass
    return BlockSchema(dict(result))
