from sqlalchemy import create_engine
from config.settings import (
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_DATABASE,
    MYSQL_USERNAME,
    MYSQL_PASSWORD
)

DATABASE_URL = (
    f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}"
    f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)

engine = create_engine(DATABASE_URL)