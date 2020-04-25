/* the block table stores information about individual blocks.
**/
CREATE TABLE btc.block (
    
    /*
     * api resource information
    **/
    -- time when the resource was created
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

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
    block_timestamp BIGINT NOT NULL,
    -- nbits is the compact form of the block target. Bitcoin uses unsigned int32.
    -- as the position of each byte is critical we use bytea here to store the data.
    -- https://en.bitcoin.it/wiki/Difficulty#How_is_difficulty_stored_in_blocks.3F
    nbits BYTEA NOT NULL,
    -- we use BIGINT for nonce since Bitcoin core uses unsigned 32bits integers and PostgreSQL does not
    -- support unsigned integers.
    nonce BIGINT NOT NULL,

    /* mining data
     * NB: we have transaction_fee = block_input - block_output
     * NB: we have transaction_fee + block_subsidy = block reward
    **/
    -- the height is the distance to the genesis block.
    height INTEGER NOT NULL,
    -- https://github.com/bitcoin/bitcoin/blob/master/src/amount.h
    -- NB: 1 BTC = 100 000 000 satoshis
    -- the amount in satoshi unlocked by the coinbase transaction when the block is mined.
    block_subsidy BIGINT NOT NULL,
    -- the value in satoshi of all inputs of this block's transactions.
    block_input BIGINT NOT NULL,
    -- the value in satoshi of all outputs of this block's transactions. 
    block_output BIGINT NOT NULL,
    -- the value in satoshi of the transaction fee.
    transaction_fee BIGINT NOT NULL,

    CONSTRAINT pk_block__block_hash PRIMARY KEY (block_hash),
    CONSTRAINT ck_block__size CHECK (size > 0),
    CONSTRAINT ck_block__transaction_counter CHECK (transaction_counter >= 0),
    CONSTRAINT ck_block__blokc_version CHECK(block_version > 0),
    CONSTRAINT ck_block__nonce CHECK(nonce >= 0),
    CONSTRAINT ck_block__height CHECK(height >= 0),
    CONSTRAINT ck_block__block_subsidy CHECK(block_subsidy >= 0),
    CONSTRAINT ck_block__block_output CHECK(block_output >= 0),
    CONSTRAINT ck_block__block_input CHECK(block_input >= 0),
    CONSTRAINT ck_block__transaction_fee CHECK(transaction_fee >= 0 AND transaction_fee = block_input - block_output)
);

CREATE INDEX idx_block__block_hash ON btc.block USING HASH (block_hash);