<div align="center">
    <img src="static/images/SmartDashLogox500.png" alt="Logo">
</div>

<h1 align="center">
    SmartDash
</h1>

<div align="center">
    <h3 align="center">A simple web application to manage your smart devices from a single dashboard</h3>
    <p align="center">
        <a href="#installation">Installation</a> •
        <a href="#configuration">Configuration</a> •
        <a href="https://github.com/t0ry003/SmartDash/wiki">Wiki</a>
    </p>

[![GitHub stars](https://img.shields.io/github/stars/t0ry003/SmartDash.svg)](https://github.com/t0ry003/SmartDash/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/t0ry003/SmartDash.svg)](https://github.com/t0ry003/SmartDash/network)
[![GitHub issues](https://img.shields.io/github/issues/t0ry003/SmartDash.svg)](https://github.com/t0ry003/SmartDash/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/t0ry003/SmartDash.svg)](https://github.com/t0ry003/SmartDash/pulls)
[![GitHub license](https://img.shields.io/github/license/t0ry003/SmartDash.svg)](https://github.com/t0ry003/SmartDash/blob/main/LICENSE)
</div>

SmartDash is a simple web application that allows you to manage your smart devices from a single dashboard. This guide will help you install and use the application.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- A supported database (e.g., MSSQL, PostgreSQL, MySQL, MariaDB, Firebird, Sybase)

### Steps

1. **Clone the repository:**

    ```sh
    git clone https://github.com/t0ry003/SmartDash.git
    cd SmartDash
    ```

2. **Create a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the database configuration:**

   Run the `app.py` script to create the `config.json` file with your database settings:

    ```sh
    python app.py
    ```

   Follow the prompts to enter your database details.

## Configuration

The `config.json` file will be created in the root directory with the following structure:

```json
{
    "db_type": "your_database_type",
    "db_name": "your_database_name",
    "db_user": "your_database_user",
    "db_password": "your_database_password",
    "db_host": "your_database_host",
    "db_port": "your_database_port",
    "db_uri": "your_database_uri"
}

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.