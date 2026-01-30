
import sqlite3
import os

from loki import queries

DB_PATH = "./db/loki.db"

conn = sqlite3.connect(DB_PATH)
middleware = conn.cursor()

def setup_database():
    check_health()

    if os.path.exists(DB_PATH):
        middleware.execute("PRAGMA user_version;")
        if middleware.fetchall():
            pass
    
    middleware.execute(queries.IMAGE_TABLE)
    middleware.execute(queries.CONTAINER_TABLE)
    middleware.execute(queries.SCRIPTS_TABLE)
    middleware.execute(queries.CMDS_TABLE)
    middleware.execute(queries.COPY_TABLE)
    middleware.execute(queries.PORTS_TABLE)
    middleware.execute(queries.EVN_TABLE)

    if not middleware.fetchone():
        raise Exception("database setup failed")

def add_image(options):
    check_options(options)
    check_health()

def add_container(options):
    check_options(options)
    check_health()

def fetch_container():
    check_health()

def fetch_image():
    check_health()

def check_health():
    middleware.execute(queries.PING)
    result = middleware.fetchone()[0]
    if result != "ok":
        raise Exception("database corrupted")

def check_options(options):
    if options is None:
        raise Exception("empty options")
