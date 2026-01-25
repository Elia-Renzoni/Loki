
'''
tables definition
'''

IMAGE_TABLE = """
CREATE TABLE IF NOT EXISTS image (
    image_id INTEGER PRIMARY KEY
    name     VARCHAR(255) UNIQUE NOT NULL
    workdir  VARCHAR(255) NOT NULL
);
"""

SCRIPTS_TABLE = """
CREATE TABLE IF NOT EXISTS scripts (
    script       VARCHAR(255) NOT NULL
    image_id     INTEGER NOT NULL
    FOREIGN KEY(image_id) REFERENCES image(image_id)
);
"""

CMDS_TABLE = """
CREATE TABLE IF NOT EXISTS cmd (
    cmd      VARCHAR(255) NOT NULL
    image_id INTEGER NOT NULL
    FOREIGN KEY(image_id) REFERENCES image(image_id)
);
"""

COPY_TABLE = """
CREATE TABLE IF NOT EXISTS copy (
    target   VARCHAR(255) NOT NULL
    image_id INTEGER NOT NULL
    FOREIGN KEY(image_id) REFERENCES image(image_id)
);
"""

PORTS_TABLE = """
CREATE TABLE IF NOT EXISTS port (
    port         INTEGER NOT NULL
    image_id     INTEGER NOT NULL
    container_id INTEGER NOT NULL
    FOREIGN KEY(image_id) REFERENCES image(image_id),
    FOREIGN KEY(container_id) REFERENCES container(container_id)
);
"""

CONTAINER_TABLE = """
CREATE TABLE IF NOT EXISTS container (
);
"""

EVN_TABLE = """
CREATE TABLE IF NOT EXISTS env (
    env_map      VARCHAR(255) NOT NULL
    container_id INTEGER NOT NULL
    FOREIGN KEY(container_id) REFERENCES container(container_id)
);
"""

'''
select definitions
'''

CHECK_IMAGE_PRESENCE = """
SELECT image_id AS image
FROM image
WHERE name = ?;
"""

CHECK_CONTAINER_PRESENCE = """
SELECT container_id AS container
FROM container
WHERE container = ?;
"""

FETCH_IMAGES = """
"""
