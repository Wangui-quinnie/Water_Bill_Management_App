# water_bill_app.py

import mysql.connector
from mysql.connector import Error
import datetime

# --- Configuration ---
# !! IMPORTANT: Update these with your MySQL connection details !!
DB_CONFIG = {
    'host': 'localhost',
    'user': 'username', # or your specific username
    'password': 'yourpassword', # replace with your MySQL password
    'database': 'rental_management'
}

# Billing constants
WATER_RATE_PER_UNIT = 130
CURRENCY_SYMBOL = 'KSH'
# -------------------

def db_connect():
    """Establishes a connection to the database."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            # print("Database connection successful.")
            return conn
    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        # Exit if we can't connect to the database, as the app is useless without it.
        exit()
    return None

def load_tenants():
    """Loads tenant data from the MySQL database."""
    conn = db_connect()
    tenants = {}
    if conn:
        cursor = conn.cursor(dictionary=True) # dictionary=True gives us dict-like rows
        cursor.execute("SELECT * FROM tenants ORDER BY unit_number")
        rows = cursor.fetchall()
        for row in rows:
            # Use unit_number as the key, just like in the JSON version
            tenants[row['unit_number']] = row
        cursor.close()
        conn.close()
    return tenants

def add_tenant():
    """Adds a new tenant to the database."""
    print("\n--- Add a New Tenant ---")
    unit = input("Enter tenant's unit number: ")
    meter_number = input("Enter tenant's water meter number: ")

    while True:
        try:
            initial_reading = int(input("Enter the initial water meter reading: "))
            if initial_reading < 0:
                print("Reading cannot be negative. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    conn = db_connect()
    if conn:
        cursor = conn.cursor()
        # Updated query to include meter_number
        query = """
            INSERT INTO tenants (unit_number, meter_number, previous_reading, current_reading) 
            VALUES (%s, %s, %s, %s)
        """
        try:
            cursor.execute(query, (unit, meter_number, initial_reading, initial_reading))
            conn.commit()
            print(f"Tenant in unit '{unit}' added successfully.")
        except Error as e:
            print(f"Error: Failed to add tenant. {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

def record_readings_and_generate_bills():
    """Records new readings, updates the DB, and generates bills."""
    tenants = load_tenants() # Get the latest data from the DB
    if not tenants:
        print("\nNo tenants found. Please add a tenant first.")
        return

    print("\n--- Record New Meter Readings ---")
    bills_to_generate = []
    updates_to_perform = []

    for unit, data in tenants.items():
        print(f"\nUnit: {unit}")
        print(f"Previous Reading: {data['previous_reading']}")
        
        while True:
            try:
                current_reading = int(input(f"Enter CURRENT reading for Unit {unit}: "))
                if current_reading < data['previous_reading']:
                    print("Error: Current reading cannot be less than the previous reading.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a whole number.")
        
        # Calculate usage and bill
        usage = current_reading - data['previous_reading']
        bill_amount = (usage * WATER_RATE_PER_UNIT)
        
        bills_to_generate.append({
            'unit': unit,
            'previous_reading': data['previous_reading'],
            'current_reading': current_reading,
            'usage': usage,
            'bill_amount': bill_amount
        })
        
        # Prepare the data for the DB update
        updates_to_perform.append({
            'unit': unit,
            'new_reading': current_reading
        })

    # --- Update the database with all new readings ---
    conn = db_connect()
    if conn:
        cursor = conn.cursor()
        update_query = "UPDATE tenants SET previous_reading = %s, current_reading = %s WHERE unit_number = %s"
        try:
            for update in updates_to_perform:
                # New previous_reading and current_reading are the same for the next cycle
                cursor.execute(update_query, (update['new_reading'], update['new_reading'], update['unit']))
            conn.commit()
            print("\nMeter readings successfully updated in the database.")
        except Error as e:
            print(f"Error updating database: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    # --- Print all the bills ---
            print("\n" + "="*40)
            print("--- Water Bills for", datetime.date.today().strftime("%B %Y"), "---")
            print("="*40)
            for bill in bills_to_generate:
                print(f"""
-----------------------------------------
           WATER BILL
-----------------------------------------
Unit:           {bill['unit']}
Meter Number:   {tenants[bill['unit']]['meter_number']}
Billing Date:   {datetime.date.today()}

Previous Reading: {bill['previous_reading']}
Current Reading:  {bill['current_reading']}
-----------------------------------------
Water Usage:      {bill['usage']} units
Usage Charge:     {CURRENCY_SYMBOL}{bill['usage'] * WATER_RATE_PER_UNIT:.2f}
-----------------------------------------
TOTAL AMOUNT DUE: {CURRENCY_SYMBOL}{bill['bill_amount']:.2f}
-----------------------------------------
""")
    
def view_tenants():
        """Displays a list of all tenants from the database."""
        tenants = load_tenants()
        print("\n--- All Tenants ---")
        if not tenants:
            print("No tenants found in the database.")
            return
            
        for unit, data in tenants.items():
            print(f"Unit: {data['unit_number']:<5} | Meter: {data['meter_number']:<10} | Last Recorded Reading: {data['current_reading']}")

def generate_bills_only():
    """Generates and displays bills using current readings, without updating readings."""
    tenants = load_tenants()
    if not tenants:
        print("\nNo tenants found. Please add a tenant first.")
        return

    print("\n" + "="*40)
    print("--- Water Bills for", datetime.date.today().strftime("%B %Y"), "---")
    print("="*40)
    for unit, data in tenants.items():
        usage = data['current_reading'] - data['previous_reading']
        bill_amount = (usage * WATER_RATE_PER_UNIT)
        print(f"""
-----------------------------------------
           WATER BILL
-----------------------------------------
Unit:           {unit}
Meter Number:   {data['meter_number']}
Billing Date:   {datetime.date.today()}

Previous Reading: {data['previous_reading']}
Current Reading:  {data['current_reading']}
-----------------------------------------
Water Usage:      {usage} units
Usage Charge:     {CURRENCY_SYMBOL}{usage * WATER_RATE_PER_UNIT:.2f}
-----------------------------------------
TOTAL AMOUNT DUE: {CURRENCY_SYMBOL}{bill_amount:.2f}
-----------------------------------------
""")

def main():
    """The main function to run the application menu."""
    while True:
        print("\n===== Water Bill Management System (MySQL) =====")
        print("1. Record Readings & Generate Bills")
        print("2. Add a New Tenant")
        print("3. View All Tenants")
        print("4. Generate Bills Only")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            record_readings_and_generate_bills()
        elif choice == '2':
            add_tenant()
        elif choice == '3':
            view_tenants()
        elif choice == '4':
            generate_bills_only()
        elif choice == '5':
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":            
    main()
