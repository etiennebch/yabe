"""SQL queries for the block blueprint.
"""
# Retrieve a single block by its id.
RETRIEVE = """
    SELECT
        id AS id_,
        ENCODE(block_hash, 'hex') AS hash_,
        size,
        transaction_counter AS transaction_count,
        block_version AS version,
        previous_hash,
        merkle_root_hash AS merkle_root,
        block_timestamp AS timestamp,
        nbits,
        -- https://en.bitcoin.it/wiki/Difficulty#How_is_difficulty_stored_in_blocks.3F
        ENCODE((nbits * 2**(8*(0x1b - 3)), 'hex') AS target,
        nonce,
        height,
        block_subsidy AS subsidy,
        block_input AS input,
        block_output AS output,
        (block_input - block_output) AS transaction_fee
    FROM btc.block
    WHERE id = :id
"""