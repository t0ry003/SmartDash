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

To be added:

- ESP32 website flasher;
- Hardware diagrams for ESP32 (SmartPlug, SmartSwitch, SmartLight, Thermostat, etc.);
- Larger solar inverters brand support;

---

## 🚀 Installation

### Target of this project

The target of this project is to create your own smart home dashboard on your old computer or Raspberry Pi. It is
designed to be lightweight and easy to set up, making it perfect for those who want to create a smart home system
without the need for expensive hardware or complex software. Since Home Assistant is a bit heavy for Raspberry Pi, this
project is designed to be lightweight and easy to set up for those who want to learn about smart home systems and create
their own dashboard. This project is not intended to be a full-fledged smart home system, but rather a starting point
for those who want to learn about smart home systems and create their own dashboard. It is designed to be modular and
extensible, allowing you to add your own features and functionality as needed.

### Prerequisites

- Python **3.10** or **3.11**
- `pip` (Python package manager)
- A supported database (**PostgreSQL**, **MSSQL**, **MySQL**, **MariaDB**, Firebird, Sybase)

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

#### Why we recommend PostgreSQL?

- **[neon.tech](https://neon.tech/)**: Neon is a serverless PostgreSQL database that allows you to create a free
  database with a single click. It is easy to set up and provides a great user experience.
- **DIY**: If you prefer to set up your own PostgreSQL database, you can do so by following the instructions on the
  official PostgreSQL website. It provides detailed documentation on how to install and configure PostgreSQL on various
  platforms.
- **Performance**: PostgreSQL is known for its high performance and scalability, making it suitable for handling large
  datasets and complex queries.

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
