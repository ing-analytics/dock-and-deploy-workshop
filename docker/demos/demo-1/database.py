import logging
import os
import pyodbc


def to_sql_server_address(server):
    """Turn the usual "host:port" into "host,port", which SQL Server expects."""
    return server.replace(":", ",")


def get_db_conn():
    server = to_sql_server_address(os.getenv("SERVER", "localhost:1433"))
    database = os.getenv("DATABASE")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    driver  = os.getenv("DRIVER", "{ODBC Driver 18 for SQL Server}")

    conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes"
    try:
        logging.info(f"CONNECTING TO DB: {database}")
        conn = pyodbc.connect(conn_str, autocommit=True) 
    except Exception as e:
        logging.error(f"NOT ABLE TO CONNECT TO DB: {e}")
        conn = None
    return conn