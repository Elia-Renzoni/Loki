
import sqlite3
import os

DB_PATH = "./db/loki.db"

conn = sqlite3.connect(DB_PATH)
middleware = conn.cursor()

def setup_database():
    check_health()

    if os.path.exists(DB_PATH):
        middleware.execute("PRAGMA user_version;")
        if middleware.fetchall():
            pass
    
    image_table = """
        CREATE TABLE image (
            id INTEGER
            name VARCHAR(255)
            copy VARCHAR(255)
            workdir VARCHAR(255)
            PRIMARY KEY(id)
        );
    """

    container_table = """
        CREATE TABLE container (
        )
    """

    scripts_table = """
        CREATE TABLE script (
        );
    """

    cmds_table = """
        CREATE TABLE action (
        );
    """

    middleware.execute(image_table)
    middleware.execute(container_table)
    middleware.execute(scripts_table)
    middleware.execute(cmds_table)

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

PING = "PRAGMA integrity_check;"
def check_health():
    middleware.execute(PING)
    result = middleware.fetchone()[0]
    if result != "ok":
        raise Exception("database corrupted")

def check_options(options):
    if options is None:
        raise Exception("empty options")
