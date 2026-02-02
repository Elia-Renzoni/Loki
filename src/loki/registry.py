
import sqlite3
import os

from loki import queries

DB_PATH = "loki.db"

conn = sqlite3.connect(DB_PATH)
middleware = conn.cursor()

def setup_database():
    check_health() 

    if os.path.exists(DB_PATH):
        middleware.execute(queries.IS_DB_USED)
        if middleware.fetchone()[0] == 1:
            return

    tables = [
            queries.IMAGE_TABLE,
            queries.CONTAINER_TABLE,
            queries.SCRIPTS_TABLE,
            queries.CMDS_TABLE,
            queries.COPY_TABLE,
            queries.PORTS_TABLE,
            queries.EVN_TABLE,
    ]

    for stmt in tables:
        try:
            middleware.execute(stmt)
        except Exception as e:
            raise Exception(f"database setup failed due to: {e}")

    middleware.execute(queries.MARK_AS_USED)

def add_image(options):
    check_options(options)
    check_health()
   
    middleware.execute(
            queries.INSERT_IMAGE,
            (options.get_image_name(), options.get_image_workdir())
    )

    image_id = middleware.lastrowid

    copy_target_tuples = [(target, image_id) for target in options.get_image_copy_targets()]
    middleware.executemany(
            queries.INSERT_COPY_TARGET,
            copy_target_tuples,
    )

    cmd_tuples = [(cmd, image_id) for cmd in options.get_image_cmds()]
    middleware.executemany(
            queries.INSERT_CMD,
            cmd_tuples,
    )

    port_tuples = [(port, image_id) for port in options.get_image_ports()]
    middleware.executemany(
            queries.INSERT_PORT,
            port_tuples,
    )

    script_tuples = [(script, image_id) for script in options.get_image_scripts()]
    middleware.executemany(
            queries.INSERT_SCRIPT,
            script_tuples,
    )

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
