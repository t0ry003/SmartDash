<div align="center">
  <img src="static/images/0.5x/Artboard%201@0.5x.png" alt="SmartDash" width="400">
</div>

<h1 align="center">SmartDash</h1>

<div align="center">
  <h3 align="center">📡 A modern web application to monitor and manage your smart devices effortlessly from a centralized dashboard.</h3>
  <p align="center">
    <a href="#installation">Installation</a> •
    <a href="#configuration">Configuration</a> •
    <a href="https://github.com/t0ry003/SmartDash/wiki">Wiki</a>
  </p>

[![GitHub Stars](https://img.shields.io/github/stars/t0ry003/SmartDash.svg)](https://github.com/t0ry003/SmartDash/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/t0ry003/SmartDash.svg)](https://github.com/t0ry003/SmartDash/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/t0ry003/SmartDash.svg)](https://github.com/t0ry003/SmartDash/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/t0ry003/SmartDash.svg)](https://github.com/t0ry003/SmartDash/pulls)
[![License](https://img.shields.io/github/license/t0ry003/SmartDash.svg)](https://github.com/t0ry003/SmartDash/blob/main/LICENSE)
</div>

---

## 📋 Overview

**SmartDash** is a lightweight, flexible, and easy-to-use web dashboard designed to manage and monitor your smart home
devices.  
Built with **Python (Flask)** and **JavaScript**, it enables you to connect to various databases and offers a
streamlined setup experience.

Key Features:

- 📱 Centralized control panel for your smart devices
- ⚡ Quick and easy database configuration
- 🧩 Modular architecture for future expansion
- 🌐 Built using Flask and modern frontend technologies

---

## 🚀 Installation

### Prerequisites

- Python **3.10** or **3.11**
- `pip` (Python package manager)
- A supported database (**MSSQL**, **PostgreSQL**, **MySQL**, **MariaDB**, Firebird, Sybase)

### Setup Instructions

1. **Clone the repository:**
    ```bash
    git clone https://github.com/t0ry003/SmartDash.git
    cd SmartDash
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # Activate the virtual environment
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. **Install required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run initial setup and database configuration:**
    ```bash
    python app.py
    ```
   This will guide you through generating a `config.json` file based on your database credentials.

---

## Database Installation
### Tested Databases
- **PostgreSQL**: PostgreSQL (https://www.postgresql.org/)
- **MSSQL**: Microsoft SQL Server (https://www.microsoft.com/en-us/sql-server/sql-server-downloads)
- **MySQL**: MySQL (https://www.mysql.com/)
- **MariaDB**: MariaDB (https://mariadb.org/)

### Database Setup
**PostgreSQL (Recommended)** - https://www.w3schools.com/postgresql/postgresql_install.php 


## ⚙️ Configuration

After the initial setup, your `config.json` file will look like this:

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
