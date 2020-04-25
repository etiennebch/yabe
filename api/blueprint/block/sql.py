"""SQL queries for the block blueprint.
"""
# Retrieve a single block by its id.
RETRIEVE = """
    SELECT
        created_at,
        block_hash AS hash,
        size,
        transaction_counter AS transaction_count,
        block_version AS version,
        previous_hash AS previous_hash,
        merkle_root_hash AS merkle_root,
        block_timestamp AS timestamp,
        nbits,
        nonce,
        height,
        block_subsidy AS subsidy,
        block_input AS input,
        block_output AS output,
        (block_input - block_output) AS transaction_fee
    FROM btc.block
    WHERE id = %(id)s
"""

# Create a block record.
CREATE = """
    INSERT INTO btc.block (
        block_hash, size, transaction_counter, block_version,
        previous_hash, merkle_root_hash, block_timestamp, nbits,
        nonce, height, block_subsidy, block_input, block_output, transaction_fee
    ) VALUES
    (
        %(hash)s, %(size)s, %(transaction_count)s, %(version)s,
        %(previous_hash)s, %(merkle_root)s, %(timestamp)s, %(nbits)s,
        %(nonce)s, %(height)s, %(subsidy)s, %(input)s, %(output)s, %(transaction_fee)s
    )
    RETURNING
        block_hash AS hash,
        size,
        transaction_counter AS transaction_count,
        block_version AS version,
        previous_hash,
        merkle_root_hash AS merkle_root,
        block_timestamp AS timestamp,
        nbits,
        nonce,
        height,
        block_subsidy AS subsidy,
        block_input AS input,
        block_output AS output,
        transaction_fee,
        created_at
"""
