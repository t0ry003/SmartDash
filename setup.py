import json
import os
import platform
import urllib

import sqlalchemy

DB_TYPES = {
    "1": ("MSSQL", "mssql+pymssql"),
    "2": ("PostgreSQL", "postgresql+psycopg2"),
    "3": ("MySQL", "mysql+pymysql"),
    "4": ("MariaDB", "mariadb+mariadbconnector"),
    "5": ("Firebird", "firebird+fdb"),
    "6": ("Sybase", "sybase+pyodbc"),
    "7": ("SmartDash", "postgresql+psycopg2")
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
        print(
            f"{BColors.FAIL}Connection failed: {e}{BColors.ENDC}\n{BColors.OKCYAN}THE DATABASE MAY BE IN TIMEOUT.{BColors.ENDC}")
        return False


def clear_screen():
    os.system("cls" if platform.system() == "Windows" else "clear")


def create_config_file():
    clear_screen()
    print(f"{BColors.HEADER}=== SmartDash Database Configuration ==={BColors.ENDC}\n")

    print(f"{BColors.UNDERLINE}Choose a database type:{BColors.ENDC}")
    for key, (name, _) in DB_TYPES.items():
        print(f"{BColors.OKCYAN}{key}. {name}{BColors.ENDC}")

    print()
    choice = input(f"{BColors.OKBLUE}Enter choice (1–7): {BColors.ENDC}").strip()

    if choice not in DB_TYPES:
        print(f"{BColors.WARNING}Invalid choice. Defaulting to SmartDash (PostgreSQL on Neon).{BColors.ENDC}")
        choice = "7"

    clear_screen()
    db_type_name, db_type_uri = DB_TYPES[choice]

    print(f"{BColors.BOLD}Selected database type: {db_type_name}{BColors.ENDC}\n")

    if choice != "7":
        db_name = input("Enter database name: ").strip()
        db_user = input("Enter username: ").strip()
        db_password = input("Enter password: ").strip()
        db_host = input("Enter host (e.g., smartdashproject.database.windows.net): ").strip()
        db_port = input("Enter port (e.g., 1433 for MSSQL, 5432 for PostgreSQL): ").strip()
    else:
        print(f"{BColors.OKCYAN}Using default credentials for SmartDash on Neon (for testing).{BColors.ENDC}")
        db_name = "neondb"
        db_user = "neondb_owner"
        db_password = "npg_94eJtlDyYBEM"
        db_host = "ep-jolly-bush-a28oyp90-pooler.eu-central-1.aws.neon.tech"
        db_port = "5432"

    encoded_password = db_password if db_type_uri == "mssql+pymssql" else urllib.parse.quote_plus(db_password)
    db_uri = f"{db_type_uri}://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"

    print(f"\n{BColors.BOLD}Testing connection to {db_type_name}...{BColors.ENDC}")
    if not test_connection(db_uri):
        print(f"{BColors.FAIL}Connection test failed. Fix issues and retry.{BColors.ENDC}")
        return None

    print(f"\n{BColors.OKGREEN}Connection successful!{BColors.ENDC}")

    confirm = input(f"\n{BColors.OKBLUE}Do you want to save this configuration? (y/n): {BColors.ENDC}").strip().lower()
    if confirm != 'y':
        print(f"{BColors.WARNING}Configuration not saved.{BColors.ENDC}")
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

    print(f"{BColors.OKGREEN}\nConfiguration saved to config.json successfully!{BColors.ENDC}")

    open_file = input(f"{BColors.OKCYAN}Would you like to open the config file location? (y/n): {BColors.ENDC}")
    if open_file.lower() == "y":
        open_config_file_location()

    return db_uri


def load_config():
    if not check_config_file():
        return None

    with open('config.json', "r") as file:
        return json.load(file)


def open_config_file_location():
    if platform.system() == "Windows":
        os.system("start .")
    elif platform.system() == "Darwin":
        os.system("open .")
    else:
        os.system("xdg-open .")
