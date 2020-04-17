# Yet another block explorer.

The purpose of the project is to build a block explorer for the bitcoin block chain.
There are many block explorers already. The rationale is that building a block explorer myself will enable me to gain a deep understand of the blockchain structure and the bitcoin ecosystem
This project aims to bring novel visualisations and ways of exploring the blockchain that do not feel clunky.
Current block explorers are a lot like Excel spreadsheet and not beginner or user friendly.

## Architecture

As I understand it, a block explorer is made of a blockchain node to participate in the network and record data as it is broadcasted to the network.

The data is stored in a database so that it can be easily searched either by an API on top of it or from a user interface.

For this project we’ll therefore need:

- a running node
- a database
- a frontend
- an API for the node to publish new events to the database
- an API for the frontend to query the database

## Storage

The blockchain is already sizable (250+ Gb) so working on efficient compression and storage could pay off.
Languages

Api will be written in Python to be developed rapidly. The frontend will be in React.The frontend must be as fast as possible since I noticed most ‘advanced’ explorers, especially those involving visualization tend to be slow.

## Competition

https://www.lopp.net/bitcoin-information/block-explorers.html

Differentiation can be found on:
UI (few competitors have clean UI)
Responsiveness (explorers tend to be slow especially when they have visualization)
Great and useful visualizations (maps, graph, charts of fees and other financial information)
Privacy. This is a big topic as users may browse their transactions.

# Setup instructions

Clone the repository and create an empty directory `data` in `db`. This directory is gitignore and holds the local database file.

```shell
git clone https://github.com/etiennebch/yabe
mkdir -p yabe/db/data
```

## Database installation

Now launch the local database (you need docker-compose installed). You'll also need the psql CLI installed to log into the database.

```shell
cd yabe/db
docker-compose up -d
psql -U postgres -p 5433 -h localhost

# required statement
CREATE DATABASE explorer ENCODING 'UTF-8';
```

## Database migration

Database migrations are handled by a dockerized Flyway, which is setup as part of the docker-compose file.
In order for migrations to run the following environment variables must be declared:

- `YABE_API_ROLENAME`
- `YABE_API_PASSWORD`
- `YABE_DB_NAME`
