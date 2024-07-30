import mysql.connector
from mysql.connector import Error
import datetime
import pandas as pd
#
def connect_to_database():
    try:
        # Using a context manager to handle the connection
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="medical_store"
        )
        return db

    except Error as e:
        # Handle connection errors
        print(f"Error: {e}")
        return None

def close_connection(connection):
    if connection:
        connection.close()

def add_to_customers(table_name, item_data):
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            query = f"INSERT INTO {table_name} VALUES (%s,%s,%s, %s, %s,%s,%s, %s, %s)"
            cursor.execute(query, item_data)
            connection.commit()
            return cursor.lastrowid

        except Error as e:
            print(f"Error adding item: {e}")

        finally:
            cursor.close()
            close_connection(connection)
                     
def add_to_inventoryitem(item_data):
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO inventoryitem (ItemCode, ItemName, QuantityAvailable, PricePerUnit, StoreID, ExpiryDate, MfgDate) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, item_data)
            connection.commit()
            return cursor.lastrowid

        except Error as e:
            print(f"Error adding item to inventory: {e}")

        finally:
            cursor.close()
            close_connection(connection)

def update_inventory_item(item_code, **updated_values):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        # Construct the SQL query to update the inventory item
        sql_query = "UPDATE inventoryitem SET "
        sql_values = []
        for key, value in updated_values.items():
            sql_query += f"{key} = %s, "
            sql_values.append(value)
        # Remove the trailing comma and space
        sql_query = sql_query[:-2]
        sql_query += " WHERE ItemCode = %s"
        sql_values.append(item_code)

        # Execute the SQL query
        cursor.execute(sql_query, tuple(sql_values))
        connection.commit()

    except mysql.connector.Error as e:
        print("Error updating inventory item:", e)

    finally:
        # Close the database connection
        if connection:
            connection.close()

def show_Records(self):#from customers table
    # Clear existing records in the table
    for record in self.table.get_children():
        self.table.delete(record)

    # Fetch all records from the database
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM customers")
            records = cursor.fetchall()

            # Insert fetched records into the table
            for record in records:
                self.table.insert("", "end", values=record)

    except Exception as e:
        print(f"Error fetching records: {e}")

    finally:
        close_connection(connection)

def fetch_next_P_id():
    try:
        # Connect to the database
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()
            # Execute query to fetch the maximum patient ID
            cursor.execute("SELECT MAX(CustomerID) FROM customers")
            result = cursor.fetchone()[0]
            # If no records exist, return 1, else return the next ID
            if result is None:
                return 1
            else:
                return result + 1
    except Error as e:
        print(f"Error fetching next patient ID: {e}")
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        close_connection(connection)

def fetch_all_inventory_items():
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM inventoryitem"
            cursor.execute(query)
            records = cursor.fetchall()
            return records
        except mysql.connector.Error as e:
            print(f"Error fetching inventory items: {e}")
        finally:
            cursor.close()
            connection.close()

 
    return None

def search_inventory_items_by_code(search_param):
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM inventoryitem WHERE ItemCode LIKE '%{search_param}%';")
            records = cursor.fetchall()
            return records
    except Exception as e:
        print(f"Error searching for inventory items: {e}")
    finally:
        close_connection(connection)

def fetch_expired_medicines():
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()
            
            # Get the current date
            current_date = datetime.datetime.now().date()
            
            # Execute SQL query to select expired medicines
            #convert current date into format yyyy-mm-dd
            current_date_2 = current_date.strftime('%Y-%m-%d')
            cursor.execute("SELECT * FROM inventoryitem WHERE ExpiryDate < %s", (current_date_2,))
            
            # Fetch all rows from the result set
            expired_medicines = cursor.fetchall()
            
            return expired_medicines
    except Exception as e:
        raise e
    finally:
        close_connection(connection)

def show_all_suppliers():
    try:
        connection = connect_to_database()  # Establish a connection to the database
        if connection:
            cursor = connection.cursor()  # Create a cursor object
            cursor.execute("SELECT * FROM supplier;")  # Execute the SQL query to retrieve all suppliers
            rows = cursor.fetchall()  # Fetch all rows from the result set
            return rows  # Return the retrieved data
    except Exception as e:
        print(f"Error retrieving suppliers: {e}")
        return []  # Return an empty list if there is an error
    finally:
        close_connection(connection)  # Close the database connection

def update_supplier(suppliers_id, **update_data):
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()
            # Construct the SET part of the SQL query based on the update_data dictionary
            set_clause = ", ".join([f"{key} = %s" for key in update_data.keys()])
            # Prepare the SQL query with placeholders for parameters
            query = f"UPDATE supplier SET {set_clause} WHERE SupplierID = %s"
            # Extract the values from the update_data dictionary
            values = list(update_data.values())
            values.append(suppliers_id)  # Append the SupplierID to the values list
            # Execute the SQL query
            cursor.execute(query, tuple(values))
            # Commit the transaction
            connection.commit()
    except Exception as e:
        print(f"Error updating supplier: {e}")
    finally:
        close_connection(connection)

def add_to_supplier(supplier_id, supplier_name, contact_info):
    # Connect to the database
    db = connect_to_database()

    if db:
        try:
            # Create a cursor object
            cursor = db.cursor()

            # Check if all fields are filled
            if supplier_id and supplier_name and contact_info:
                # SQL query to insert data into the table
                query = "INSERT INTO supplier (SupplierID, SupplierName, ContactInfo) VALUES (%s, %s, %s)"
                values = (supplier_id, supplier_name, contact_info)

                # Execute the query
                cursor.execute(query, values)

                # Commit changes to the database
                db.commit()


        except Error as e:
            # Handle database errors
            print(f"Error saving supplier information: {e}")

        finally:
            # Close the cursor and database connection
            if cursor:
                cursor.close()
            close_connection(db)

    else:
        print("Error: Unable to establish database connection")

def fetch_record_by_C_ID(CustomerID):
    try:
        # Connect to the database
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()

            # Execute the query to fetch the record based on the provided patient ID
            cursor.execute("SELECT * FROM customers WHERE CustomerID = %s", (CustomerID,))
            
            # Fetch the record
            record = cursor.fetchone()

            # Return the record
            return record
    except mysql.connector.Error as e:
        print("Error fetching record:", e)
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()          
    
def fetch_medicine_list():
    # Connect to the database
    connection = connect_to_database()

    if connection:
        try:
            # Creating a cursor object using the cursor() method
            cursor = connection.cursor()

            # Preparing query to fetch all medicine names
            query = "SELECT ItemName FROM inventoryitem"

            # Executing the SQL query
            cursor.execute(query)

            # Fetching all rows from the result set
            rows = cursor.fetchall()

            # Extracting medicine names from the rows
            medication_names = [row[0] for row in rows]

            return medication_names

        except Error as e:
            print(f"Error fetching medicine list: {e}")

        finally:
            # Closing the cursor and connection
            cursor.close()
            close_connection(connection)
    else:
        print("Failed to connect to the database.")
        return None

def get_next_order_id():
    try:
        # Establish a connection to the MySQL database
        connection = connect_to_database()

        # Create a cursor object
        cursor = connection.cursor()

        # Query to get the maximum order_id from the bills table
        query = "SELECT MAX(order_id) FROM bills"

        # Execute the query
        cursor.execute(query)

        # Fetch the result
        result = cursor.fetchone()

        # Close the cursor and database connection
        close_connection(connection)

        # Increment the maximum order_id by 1
        next_order_id = result[0] + 1 if result[0] else 1

        return next_order_id

    except Exception as e:
        print("Error fetching next order ID:", e)
        return None

def save_to_database(order_id, customer_name, customer_phone, bill_date, total_amount, CustomerID):
    try:
        # Establish a connection to the database
        connection = connect_to_database()
        
        if connection:
            # Create a cursor object using the cursor() method
            cursor = connection.cursor()

            # Define the SQL query to insert data into the 'bills' table
            query = "INSERT INTO bills (order_id, customer_name, customer_phone, bill_date, total_amount, CustomerID) VALUES (%s, %s, %s, %s, %s, %s)"

            # Define the values to be inserted
            values = (order_id, customer_name, customer_phone, bill_date, total_amount, CustomerID)

            # Execute the SQL query with the provided values
            cursor.execute(query, values)

            # Commit the transaction
            connection.commit()

            print("Data saved to database successfully!")

    except Exception as e:
        # Rollback in case of any error
        connection.rollback()
        print(f"Error in Saving to database: {e}")

    finally:
        # Close the cursor and connection
        cursor.close()
        close_connection(connection)

def fetch_latest_CustomerID(customer_name, customer_phone):
    # Connect to the database
    connection = connect_to_database()

    if connection:
        try:
            # Creating a cursor object using the cursor() method
            cursor = connection.cursor()

            # Preparing query to fetch the customer ID
            query = "SELECT CustomerID FROM customers WHERE Name = %s AND Phone = %s ORDER BY CustomerID DESC LIMIT 1"

            # Executing the SQL query with the provided customer name and phone number
            cursor.execute(query, (customer_name, customer_phone))

            # Fetching the customer ID from the result set
            row = cursor.fetchone()

            if row:
                # If customer ID exists, return it
                return row[0]
            else:
                # If customer ID doesn't exist, call add_new_customer function
                CustomerID = add_new_customer(customer_name, customer_phone)
                return CustomerID

        except Error as e:
            print(f"Error fetching customer ID: {e}")

        finally:
            # Closing the cursor and connection
            cursor.close()
            close_connection(connection)
    else:
        print("Failed to connect to the database.")
        return None
    
def add_new_customer(customer_name, customer_phone):
    # Connect to the database
    connection = connect_to_database()

    if connection:
        try:
            # Creating a cursor object using the cursor() method
            cursor = connection.cursor()

            # Get the next customer ID
            next_CustomerID = get_next_CustomerID()

            # Preparing query to insert a new customer into the database
            query = "INSERT INTO customers (CustomerID, Name, Phone) VALUES (%s, %s, %s)"

            # Executing the SQL query with the provided customer ID, name, and phone number
            cursor.execute(query, (next_CustomerID, customer_name, customer_phone))

            # Commit the transaction
            connection.commit()

            return next_CustomerID

        except Error as e:
            print(f"Error adding new customer: {e}")

        finally:
            # Closing the cursor and connection
            cursor.close()
            close_connection(connection)
    else:
        print("Failed to connect to the database.")
        return None

def get_next_CustomerID():
    # Connect to the database
    connection = connect_to_database()

    if connection:
        try:
            # Creating a cursor object using the cursor() method
            cursor = connection.cursor()

            # Preparing query to fetch the maximum customer ID and increment it
            query = "SELECT MAX(CustomerID) FROM customers"

            # Executing the SQL query to fetch the maximum customer ID
            cursor.execute(query)

            # Fetching the maximum customer ID from the result set
            row = cursor.fetchone()

            # If maximum customer ID exists, increment it by 1, else start from 1
            if row and row[0]:
                next_CustomerID = row[0] + 1
            else:
                next_CustomerID = 1

            return next_CustomerID

        except Error as e:
            print(f"Error fetching next customer ID: {e}")

        finally:
            # Closing the cursor and connection
            cursor.close()
            close_connection(connection)
    else:
        print("Failed to connect to the database.")
        return None
        
def fetch_sales_data(start_date, end_date):
    # Establish a connection to the MySQL database
    try:
        connection = connect_to_database()

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)

            # SQL query to fetch sales data between the provided date range
            query = "SELECT total_amount FROM bills WHERE bill_date BETWEEN %s AND %s"
            cursor.execute(query, (start_date, end_date))

            # Fetch all rows of the result set
            sales_data = cursor.fetchall()

            return sales_data

    except mysql.connector.Error as e:
        print(f"Error accessing MySQL database: {e}")

    finally:
        close_connection(connection)

    return None

def fetch_daily_sales(start_date, end_date):
    try:
        # Establish a connection to the MySQL database
        connection = connect_to_database()

        if connection.is_connected():
            cursor = connection.cursor()

            # Delete the contents of the daily_sales table
            delete_query = "DELETE FROM daily_sales"
            cursor.execute(delete_query)
            connection.commit()

            # Calculate daily sales and insert into the daily_sales table
            calculate_query = """
                INSERT INTO daily_sales (date, sale)
                SELECT bill_date, SUM(total_amount) AS sale
                FROM bills
                GROUP BY bill_date
                ORDER BY bill_date ASC
            """
            cursor.execute(calculate_query)
            connection.commit()
            
            cursor = connection.cursor(dictionary=True)

            # SQL query to fetch daily sales data between the provided date range
            query = "SELECT * FROM daily_sales WHERE date BETWEEN %s AND %s"
            cursor.execute(query, (start_date, end_date))

            # Fetch all rows of the result set
            daily_sales_data = cursor.fetchall()
            
            # convert it into pandas dataframe
            daily_sales_data = pd.DataFrame(daily_sales_data)

            return daily_sales_data
            
    except mysql.connector.Error as e:
        # Handle any errors that occur during the database operation
        print(f"An error occurred: {e}")

    finally:
        close_connection(connection)

def calculate_monthly_sales(year, month_number):
    try:
        # Establish a connection to the MySQL database
        connection = connect_to_database()

        if connection.is_connected():
            cursor = connection.cursor()

            # Delete the contents of the monthly_sales table for the specified month and year
            delete_query = "DELETE FROM monthly_sales WHERE year = %s AND month = %s"
            cursor.execute(delete_query, (year, month_number))
            connection.commit()

            # Calculate monthly sales and insert into the monthly_sales table
            calculate_query = """
                INSERT INTO monthly_sales (year, month, total_sales)
                SELECT YEAR(bill_date) AS year, MONTH(bill_date) AS month, SUM(total_amount) AS total_sales
                FROM bills
                WHERE YEAR(bill_date) = %s AND MONTH(bill_date) = %s
                GROUP BY YEAR(bill_date), MONTH(bill_date)
            """
            cursor.execute(calculate_query, (year, month_number))
            connection.commit()


            
    except mysql.connector.Error as e:
        # Handle any errors that occur during the database operation
        print(f"An error occurred: {e}")

    finally:
        close_connection(connection)

def fetch_monthly_sales(start_date, end_date):
    calculate_monthly_sales(start_date.year, start_date.month)
    start_month_year = start_date.strftime('%Y-%m')
    end_month_year = end_date.strftime('%Y-%m')
    
    try:
        # Establish a connection to the MySQL database
        connection = connect_to_database()

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)

            # Define the SQL query to fetch monthly sales data within the specified range
            sql_query = """
                SELECT year, month, total_sales
                FROM monthly_sales
                WHERE CONCAT(year, '-', LPAD(month, 2, '0')) BETWEEN %s AND %s
            """
            cursor.execute(sql_query, (start_month_year, end_month_year))

            # Fetch all rows of the result set
            monthly_sales_data = cursor.fetchall()

            return monthly_sales_data
            
    except mysql.connector.Error as e:
        # Handle any errors that occur during the database operation
        print(f"An error occurred: {e}")

    finally:
        close_connection(connection)

    
def insert_employee(emp_username, first_name, last_name, phone_number, address, dob, date_of_hire, salary, access_level):
    try:
        # Connect to the database
        conn = connect_to_database()
        
        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # SQL query to insert employee data into the Employee table
        insert_query = "INSERT INTO Employee (emp_username, first_name, last_name, phone_number, address, date_of_birth, date_of_hire, salary, access_level) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        
        # Tuple containing employee data
        employee_data = (emp_username, first_name, last_name, phone_number, address, dob, date_of_hire, salary, access_level)

        # Execute the SQL query with employee data
        cursor.execute(insert_query, employee_data)

        # Commit changes to the database
        conn.commit()

        print("Employee inserted successfully!")

    except mysql.connector.Error as error:
        print("Error inserting employee:", error)

    finally:
        # Close cursor and database connection
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            close_connection(conn)


def get_employee(emp_username):
    try:
        # Connect to the database
        conn = connect_to_database()

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # SQL query to fetch employee details based on emp_username
        select_query = "SELECT * FROM Employee WHERE emp_username = %s"
        
        # Execute the SQL query with the emp_username parameter
        cursor.execute(select_query, (emp_username,))

        # Fetch the result
        result = cursor.fetchone()

        if result:
            # Return the fetched employee details
            return result
        else:
            print("No employee found with emp_username:", emp_username)
            return None

    except mysql.connector.Error as error:
        print("Error fetching employee details:", error)

    finally:
        # Close cursor and database connection
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            close_connection(conn)

    
def get_all_employees():
    try:
        # Connect to the database
        conn = connect_to_database()

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # SQL query to fetch all employee details
        select_query = "SELECT * FROM Employee"

        # Execute the SQL query
        cursor.execute(select_query)

        # Fetch all rows from the result set
        employee_details = cursor.fetchall()

        return employee_details

    except mysql.connector.Error as error:
        print("Error fetching employee details:", error)
        return None

    finally:
        # Close cursor and database connection
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            close_connection(conn)



    