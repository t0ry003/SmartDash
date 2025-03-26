import json
import urllib

import sqlalchemy

DB_TYPES = {
    "1": ("MSSQL", "mssql+pymssql"),
    "2": ("PostgreSQL", "postgresql+psycopg2"),
    "3": ("MySQL", "mysql+pymysql"),
}


class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def check_config_file():
    try:
        with open('config.json', 'r') as f:
            return True
    except FileNotFoundError:
        return False


def test_connection(db_uri):
    try:
        engine = sqlalchemy.create_engine(db_uri)
        with engine.connect() as conn:
            conn.execute(sqlalchemy.sql.text("SELECT 1;"))
        print(f"{BColors.OKGREEN}Connection successful!{BColors.ENDC}")
        return True
    except Exception as e:
        print(f"{BColors.FAIL}Connection failed: {e}{BColors.ENDC}")
        return False


def create_config_file():
    print(f"{BColors.HEADER}Choose a database type: {BColors.ENDC}")
    for key, (name, _) in DB_TYPES.items():
        print(f"{key}. {name}")

    choice = input("Enter choice (1/2/3): ").strip()
    if choice not in DB_TYPES:
        print("Invalid choice, defaulting to MSSQL.")
        choice = "1"

    db_name = input("Enter database name: ")
    db_user = input("Enter username: ")
    db_password = input("Enter password: ")
    db_host = input("Enter host (e.g., smartdashproject.database.windows.net): ")
    db_port = input("Enter port (e.g., 1433 for MSSQL, 3306 for MySQL, 5432 for PostgreSQL): ")

    db_type_name, db_type_uri = DB_TYPES[choice]

    # Only encode password for MySQL and PostgreSQL, not MSSQL
    encoded_password = db_password if db_type_uri == "mssql+pymssql" else urllib.parse.quote_plus(db_password)

    # Construct the correct database URI
    db_uri = f"{db_type_uri}://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"

    print(f"\nTesting connection to {db_type_name}...")
    if not test_connection(db_uri):
        print(f"{BColors.WARNING}Fix the connection issues before proceeding.{BColors.ENDC}")
        return None

    config = {
        "db_type": db_type_uri,
        "db_name": db_name,
        "db_user": db_user,
        "db_password": db_password,
        "db_host": db_host,
        "db_port": db_port,
        "db_uri": db_uri
    }

    with open('config.json', "w") as file:
        json.dump(config, file, indent=4)

    print(f"{BColors.OKGREEN}Configuration saved successfully!{BColors.ENDC}")

    open_file = input("Would you like to open the config file location? (y/n): ")
    if open_file.lower() == "y":
        open_config_file_location()

    return db_uri


def load_config():
    if not check_config_file():
        return None

    with open('config.json', "r") as file:
        return json.load(file)


def open_config_file_location():
    import os
    import platform
    if platform.system() == "Windows":
        os.system("start .")
    elif platform.system() == "Darwin":
        os.system("open .")
    else:
        os.system("xdg-open .")

# Connect to your remote MySQL database
# server: smartdashproject.database.windows.net
# port: 1433
# DB_name: smartdash
# username: smartdashadmin
# password: a7MgNwjiq_fs6&2
