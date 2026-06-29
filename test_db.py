from sqlalchemy import text

from config.database import engine

try:

    with engine.connect() as conn:

        result = conn.execute(text("SELECT VERSION();"))

        print("Connected Successfully!")

        print(result.fetchone())

except Exception as e:

    print(e)