import logging
import os
import psycopg2


def split_host_port(server, default_port=5432):
    """Split "host:port" into ("host", port). The port is optional."""
    host, _, port = server.partition(":")
    return host, int(port) if port else default_port


def get_db_conn():
    host, port = split_host_port(os.getenv("SERVER", "localhost:5432"))
    database = os.getenv("DATABASE")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    try:
        logging.info(f"CONNECTING TO DB: {database}")
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=database,
            user=username,
            password=password,
            connect_timeout=5,
        )
        conn.autocommit = True
    except Exception as e:
        logging.error(f"NOT ABLE TO CONNECT TO DB: {e}")
        conn = None
    return conn
