import os
import json
import psycopg2

def get_db_connection(config_file="config.json"):
    with open(config_file) as f:
        config = json.load(f)
    
    db_password = os.getenv("db_password")
    if db_password is None:
        raise ValueError("db_password environment variable is missing!")

    conn = psycopg2.connect(
        dbname=config["dbname"],
        user=config["user"],
        password=db_password,
        host=config["host"],
        port=config["port"]
    )

    return conn

