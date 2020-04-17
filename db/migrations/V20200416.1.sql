/* the block table stores information about individual blocks.
**/
CREATE TABLE btc.block (
    
    id INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY (START WITH 1001 NO CYCLE),
    block_hash BYTEA NOT NULL,

    -- the size of the block in bytes. A block is valid under consensus rules if less than 1Mb.
    size INTEGER NOT NULL,

    -- according to Bitcoin core, the count of transactions can be up to uint64
    -- https://en.bitcoin.it/wiki/Protocol_documentation#Variable_length_integer
    -- however it is unlikely in the short term to be as large as the consensus is to reject blocks
    -- of more than 1Mb in size. Since the header alone is 80 bytes, that means less than 15k transactions
    transaction_counter INTEGER NOT NULL,

    /* header data
     * https://en.bitcoin.it/wiki/Block_hashing_algorithm
     * https://github.com/bitcoin/bitcoin/blob/master/src/primitives/block.h
    **/
    -- https://bitcoin.org/en/developer-reference#block-versions
    block_version INTEGER NOT NULL,
    -- hash of the previous block
    previous_hash BYTEA NOT NULL,
    -- merke root of the transactions contained in this block
    merkle_root_hash BYTEA NOT NULL,
    -- we don't care about the time zone as the timestamp is always obtained as seconds since unix epoch.
    block_timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    -- we use BIGINT for nbits and nonce since Bitcoin core uses unsigned 32bits integers and PostgreSQL does not
    -- support unsigned integers. nbits is the compact form of the difficulty target
    -- https://en.bitcoin.it/wiki/Difficulty#How_is_difficulty_stored_in_blocks.3F
    nbits BIGINT NOT NULL,
    nonce BIGINT NOT NULL,

    /* mining data
     * NB: we have transaction_fees = block_input - block_output
     * NB: we have transaction_fees + block_subsidy = block reward
    **/
    -- the height is the distance to the genesis block.
    height INTEGER NOT NULL,
    -- https://github.com/bitcoin/bitcoin/blob/master/src/amount.h
    -- NB: 1 BTC = 100 000 000 satoshis
    -- the amount in satoshi unlocked by the coinbase transaction when the block is mined.
    block_subsidy BIGINT NOT NULL,
    -- the value in satoshi of all inputs of this block's transactions
    block_input BIGINT NOT NULL,
    -- the value in satoshi of all outputs of this block's transactions. 
    block_output BIGINT NOT NULL,

    CONSTRAINT pk_block__block_id PRIMARY KEY (id)
);

CREATE INDEX idx_block__block_hash ON btc.block USING HASH (block_hash);