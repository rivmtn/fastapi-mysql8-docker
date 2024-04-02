import os

HOSTNAME = "host.docker.internal"
USERNAME = "root"
PASSWORD = "password"
PORT = 3306
DATABASE = "mydb"
CHARSET = "utf8mb4"
DB_URL = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}"
ROOT_CTX = os.path.dirname(__file__)
