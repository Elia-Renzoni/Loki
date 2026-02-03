
'''
tables definition
'''

IMAGE_TABLE = """
CREATE TABLE IF NOT EXISTS image (
    image_id INTEGER PRIMARY KEY,
    name     VARCHAR(255) UNIQUE NOT NULL,
    workdir  VARCHAR(255) NOT NULL,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
);
"""

SCRIPTS_TABLE = """
CREATE TABLE IF NOT EXISTS script (
    script_code  VARCHAR(255) NOT NULL,
    image_id     INTEGER NOT NULL,
    FOREIGN KEY(image_id) REFERENCES image(image_id)
);
"""

CMDS_TABLE = """
CREATE TABLE IF NOT EXISTS cmd (
    cmd      VARCHAR(255) NOT NULL,
    image_id INTEGER NOT NULL,
    FOREIGN KEY(image_id) REFERENCES image(image_id)
);
"""

COPY_TABLE = """
CREATE TABLE IF NOT EXISTS copy (
    target   VARCHAR(255) NOT NULL,
    image_id INTEGER NOT NULL,
    FOREIGN KEY(image_id) REFERENCES image(image_id)
);
"""

PORTS_TABLE = """
CREATE TABLE IF NOT EXISTS port (
    port         INTEGER NOT NULL,
    image_id     INTEGER,
    container_id INTEGER,
    FOREIGN KEY(image_id) REFERENCES image(image_id),
    FOREIGN KEY(container_id) REFERENCES container(container_id)
);
"""

CONTAINER_TABLE = """
CREATE TABLE IF NOT EXISTS container (
    container_id    INTEGER PRIMARY KEY,
    container_name  VARCHAR(255) UNIQUE NOT NULL,
    mount           VARCHAR(255) NOT NULL,
    timestamp       TEXT DEFAULT CURRENT_TIMESTAMP
);
"""

EVN_TABLE = """
CREATE TABLE IF NOT EXISTS env (
    env_map      VARCHAR(255) NOT NULL,
    container_id INTEGER NOT NULL,
    FOREIGN KEY(container_id) REFERENCES container(container_id)
);
"""

'''
select definitions
'''
FETCH_ALL_IMAGES = """
SELECT image.name, 
       image.workdir, 
       image.timestamp, 
       script.script_code, 
       copy.target, 
       port.port, 
       cmd.cmd
FROM image
LEFT JOIN script ON script.image_id = image.image_id
LEFT JOIN cmd ON cmd.image_id = image.image_id
LEFT JOIN copy ON copy.image_id = image.image_id
LEFT JOIN port ON port.image_id = image.image_id;
"""

FETCH_IMAGE = """
SELECT image.name, 
       image.workdir, 
       image.timestamp, 
       script.script_code, 
       copy.target, 
       port.port, 
       cmd.cmd
FROM image
LEFT JOIN script ON script.image_id = image.image_id
LEFT JOIN cmd ON cmd.image_id = image.image_id
LEFT JOIN copy ON copy.image_id = image.image_id
LEFT JOIN port ON port.image_id = image.image_id
WHERE image.name = ?;
"""

FETCH_CONTAINER = """
SELECT container.container_name, 
       container.mount, 
       container.timestamp, 
       port,port, 
       env.env_map
FROM container
LEFT JOIN port ON port.container_id = container.container_id
LEFT JOIN env ON env.container_id = container.container_id
WHERE container.name = ?;
"""

FETCH_ALL_CONTAINERS = """
SELECT container.container_name, 
       container.mount, 
       container.timestamp, 
       port,port, 
       env.env_map
FROM container
LEFT JOIN port ON port.container_id = container.container_id
LEFT JOIN env ON env.container_id = container.container_id;
"""

'''
pragmas
'''

PING = """
PRAGMA integrity_check;
"""

MARK_AS_USED = """
PRAGMA user_version = 1;
"""

IS_DB_USED = """
PRAGMA user_version;
"""

'''
insert definitions
'''

INSERT_IMAGE = """
INSERT INTO image (name, workdir) VALUES (?, ?);
"""

INSERT_COPY_TARGET = """
INSERT INTO copy (target, image_id) VALUES (?, ?);
"""

INSERT_CMD = """
INSERT INTO cmd (cmd, image_id) VALUES (?, ?);
"""

INSERT_PORT = """
INSERT INTO port (port, image_id) VALUES (?, ?);
"""

INSERT_SCRIPT = """
INSERT INTO script (script_code, image_id) VALUES (?, ?);
"""

INSERT_CONTAINER = """
INSERT INTO container (container_name, mount) VALUES (?, ?);
"""

INSERT_ENV_VARIABLE = """
INSERT INTO env (env_map, container_id) VALUES (?, ?);
"""

INSERT_PORT_CONTAINER = """
INSERT INTO port (port, container_id) VALUES (?, ?);
"""
