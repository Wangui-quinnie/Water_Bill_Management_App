# Water Bill Management App

A simple command-line application for managing water meter readings, tenants, and generating water bills for a rental property. This app uses a MySQL database to store tenant and meter reading data.

## Features

- Add new tenants to the system
- Record new water meter readings for each tenant
- Automatically calculate and generate water bills
- View all tenants and their last recorded readings
- Data is stored and managed in a MySQL database

## Requirements

- Python 3.7+
- MySQL Server
- `mysql-connector-python` package

## Setup Instructions

### 1. Clone or Download the Project

Place the project folder (e.g., `Water_Bill_App`) on your computer.

### 2. Create and Activate a Virtual Environment (Recommended)

Open a terminal in the project directory and run:

```bash
python -m venv venv
# On Windows Command Prompt:
venv\Scripts\activate
# On Bash (Git Bash, WSL, etc.):
source venv/Scripts/activate
```

### 3. Install Dependencies

```bash
python3 -m pip install mysql-connector-python
```

### 4. Set Up the MySQL Database

1. **Start your MySQL server.**
2. **Create the database and table:**

```sql
CREATE DATABASE rental_management;

USE rental_management;

CREATE TABLE tenants (
    unit_number varchar(10) PRIMARY KEY,
    meter_number varchar(50),
    previous_reading int NOT NULL,
    current_reading int NOT NULL,
    created_at timestamp 
    updated_at timestamp
);
```

3. **Update your MySQL credentials in `water_bill_app.py`:**

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root', # your MySQL username
    'password': 'your_password', # your MySQL password
    'database': 'rental_management'
}
```

### 5. Run the Application

```bash
python3 water_bill_app.py
```

## Usage

You will see a menu with options:

1. **Record Readings & Generate Bills**: Enter new meter readings for each tenant and generate bills.
2. **Add a New Tenant**: Add a new tenant to the database.
3. **View All Tenants**: Display all tenants and their last recorded readings.
4. **Generate Bills Only**: Display all bills.
4. **Exit**: Quit the application.

Follow the prompts to interact with the system.

## Security Note

- **Never share your database password publicly.** Consider using environment variables or a `.env` file for production use.

## Troubleshooting

- **ModuleNotFoundError: No module named 'mysql'**  
  Install the connector with:  
  `pip install mysql-connector-python`
  `python3 -m pip install mysql-connector-python` (This guarantees the package installs for that exact interpreter.)

- **Can't connect to MySQL**  
  - Ensure your MySQL server is running.
  - Double-check your credentials in `DB_CONFIG`.

- **Virtual environment activation issues**  
  - On Windows Command Prompt: `venv\Scripts\activate`
  - On Bash: `source venv/Scripts/activate`

## License

This project is for Warugongo Enterprises.

---

**Author:** Winfred Wangui
**Contact:** w.wangui@ymail.com
