import os
from datetime import datetime

import psycopg
from psycopg import sql


def get_db_connection():
    """
    Connect to Neon/Postgres using a DATABASE_URL (or NEON_DATABASE_URL) environment variable.
    If sslmode is not present, it will be enforced (Neon requires TLS).
    """
    dsn = os.getenv("DATABASE_URL")
    if not dsn:
        raise RuntimeError(
            "DATABASE_URL not set. Provide your Neon connection string."
        )

    # Ensure we connect over TLS by default
    if dsn.startswith("postgres") and "sslmode=" not in dsn:
        sep = "&" if "?" in dsn else "?"
        dsn = f"{dsn}{sep}sslmode=require"

    return psycopg.connect(dsn)


def init_table(table_name: str):
    """Create the table if it does not exist, matching the SQLite schema as closely as possible."""
    print(f"Attempting connection to database for table: {table_name}...")
    with get_db_connection() as con:
        with con.cursor() as cur:
            cur.execute(
                sql.SQL(
                    '''CREATE TABLE IF NOT EXISTS {} (
                        id BIGSERIAL PRIMARY KEY,
                        lastcount INTEGER,
                        percent INTEGER,
                        "timestamp" TIMESTAMPTZ,
                        dayofweek INTEGER,
                        hour SMALLINT
                    )'''
                ).format(sql.Identifier(table_name))
            )
            con.commit()


def tables_exist(table_names):
    """Return True if all tables in table_names exist in the current schema (usually 'public')."""
    if not table_names:
        return True

    print("Attempting connection to database to verify tables...")
    with get_db_connection() as con:
        with con.cursor() as cur:
            for table_name in table_names:
                cur.execute(
                    """
                    SELECT EXISTS (
                        SELECT 1 FROM information_schema.tables
                        WHERE table_schema = current_schema()
                          AND table_name = %s
                    );
                    """,
                    (table_name,),
                )
                exists = cur.fetchone()[0]
                if not exists:
                    return False
            return True


def insert_new_data(scraped_data):
    """
    Accepts scraped_data as a dict where each key is a facility name and the corresponding value
    is a list: [last_count, percent, is_closed]. Inserts a new row into the 
    table corresponding to each facility.
    """
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    # Use weekday() where Monday=0, Sunday=6
    dayofweek = now.weekday()
    hour = int(now.strftime("%H"))

    for facility, values in scraped_data.items():
        last_count, percent, is_closed = values

        print(f"Attempting connection to database for facility: {facility}...")
        with get_db_connection() as con:
            print("Successful connection!")
            with con.cursor() as cur:
                print("Attempting to insert new data...")
                cur.execute(
                    sql.SQL(
                        'INSERT INTO {} (lastcount, percent, "timestamp", dayofweek, hour)\n'
                        "VALUES (%s, %s, %s, %s, %s)"
                    ).format(sql.Identifier(facility)),
                    (last_count, percent, timestamp, dayofweek, hour),
                )
                con.commit()
                print(f"Successful insertion for facility: {facility}!")


def get_average_for_day(dayofweek):
    # Connect to database
    print("Attempting connection to database...")
    with get_db_connection() as con:
        print("Successful connection!")
        with con.cursor() as cur:
            # Find values for day of week
            print("Attempting to find data...")
            cur.execute(
                """
                SELECT hour, AVG(percent) AS avg_percentage
                FROM helen_newman 
                WHERE dayofweek = %s
                GROUP BY hour
                ORDER BY hour;
                """,
                (dayofweek,),
            )

            data = cur.fetchall()

    if data:
        print("Was able to find!")

    return data


def get_average_for_day_hour(dayofweek: int, hour: str) -> int | None:
    # Connect to database
    print("Attempting connection to database...")
    with get_db_connection() as con:
        print("Successful connection!")
        with con.cursor() as cur:
            # Find values for day of week
            print("Attempting to find data...")
            cur.execute(
                """
                SELECT AVG(percent)
                FROM helen_newman
                WHERE dayofweek = %s AND hour = %s;
                """,
                (
                    dayofweek,
                    int(hour) if isinstance(hour, str) and hour.isdigit() else hour,
                ),
            )

            row = cur.fetchone()

    avg = row[0] if row else None

    if avg is not None:
        print("Was able to find!")

    return avg


def clean_data(schedule, table):
    with get_db_connection() as con:
        with con.cursor() as cur:
            # Get the hours for the given table
            open_hour, close_hour = schedule[table]

            # Delete rows that are outside the operating hours
            cur.execute(
                sql.SQL('DELETE FROM {} WHERE hour < %s OR hour >= %s').format(
                    sql.Identifier(table)
                ),
                (open_hour, close_hour),
            )

            con.commit()


if __name__ == "__main__":
    pass
