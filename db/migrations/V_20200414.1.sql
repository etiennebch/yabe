CREATE ROLE ${api_rolename} NOSUPERUSER NOCREATEDB NOCREATEROLE LOGIN ENCRYPTED PASSWORD ${api_password};

CREATE DATABASE ${database_name} ENCODING 'UTF-8';

/* the btc schema stores information about the Bitcoin blockchain.
**/
CREATE SCHEMA btc;

/* grant privileges
**/
GRANT CONNECT ON DATABASE ${database_name} TO ${api_rolename};
GRANT USAGE ON SCHEMA btc TO ${api_rolename};

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA btc TO ${api_rolename};
GRANT USAGE ON ALL SEQUENCES IN SCHEMA btc TO ${api_rolename};

/* grant default privileges for future objects
**/
ALTER DEFAULT PRIVILEGES FOR ${api_rolename} IN SCHEMA btc GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO ${api_rolename};
ALTER DEFAULT PRIVILEGES FOR ${api_rolename} IN SCHEMA btc USAGE ON SEQUENCES TO ${api_rolename};