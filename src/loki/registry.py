
import sqlite3
import os
from dataclasses import dataclass
from datetime import datetime, timezone


from loki import queries

DB_PATH = "loki.db"

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
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

    middleware.execute(
            queries.INSERT_CONTAINER,
            (
                options.get_container_name(), 
                options.get_container_mount()
            )
    )

    container_id = middleware.lastrowid

    if options.get_container_envs() is not None:
        env_tuples = [(env, container_id) for env in options.get_container_envs()]
        middleware.executemany(
                queries.INSERT_ENV_VARIABLE,
                env_tuples
        )


    if options.get_container_ports() is not None:
        port_tuples = [(port, container_id) for port in options.get_container_ports()]

        middleware.executemany(
                queries.INSERT_PORT_CONTAINER,
                port_tuples
        )

def fetch_container(container_name):
    check_health()

    # take a snaphost of all the stored containers
    if container_name == "all":
        middleware.execute(queries.FETCH_ALL_CONTAINERS)
        rows = middleware.fetchall()
        results = []
        for row in rows:
            data = dict(row)
            data['timestamp'] = time_since(data['timestamp'])
            results.append(data)
        return results

    # take a snapshot of a specific container
    middleware.execute(
            queries.FETCH_CONTAINER,
            (container_name,)
    )
    rows = middleware.fetchall()
    data = dict(rows[0])
    data['timestamp'] = time_since(data['timestamp'])
    return [data]

def fetch_image(image_name):
    check_health()

    if image_name is None:
        raise Exception("empty paramether")

    # take a snapshot of all the stored images
    if image_name == "all":
        middleware.execute(queries.FETCH_ALL_IMAGES)
        rows = middleware.fetchall()
        results = []
        for row in rows:
            data = dict(row)
            data['timestamp'] = time_since(data['timestamp'])
            results.append(data)
        return results

    # take a snaphost of a specific image
    middleware.execute(
            queries.FETCH_IMAGE,
            (image_name,)
    )
    rows = middleware.fetchall()
    data = dict(rows[0])
    data['timestamp'] = time_since(data['timestamp'])
    return [data]

def check_health():
    middleware.execute(queries.PING)
    result = middleware.fetchone()[0]
    if result != "ok":
        raise Exception("database corrupted")

def check_options(options):
    if options is None:
        raise Exception("empty options")

# TODO-> next patch
def calculate_size():
    pass

@dataclass(frozen=True)
class TimeSince:
    seconds: int
    minutes: int
    hours: int
    days: int


def time_since(latest_timestamp):
    created = datetime.strptime(latest_timestamp, "%Y-%m-%d %H:%M:%S").replace(
        tzinfo=timezone.utc
    )
    now = datetime.now(timezone.utc)

    delta = now - created
    total_seconds = int(delta.total_seconds())

    return TimeSince(
        seconds=total_seconds,
        minutes=total_seconds // 60,
        hours=total_seconds // 3600,
        days=delta.days,
    )
