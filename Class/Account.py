from flask import session
import mysql.connector

## This is ENTITY
class Account:
    def __init__(self, profile_type, email, password):
        self.profile_type = profile_type
        self.email = email
        self.password = password

    def create_connection():
        return mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root',
            database = 'flask_app'
        )

    def verify_login(profile_type, email, password):
        conn = Account.create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE profile = %s AND email = %s', (profile_type, email))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        # Extract the plain text password from the database
        db_password = result[2]

        # Check if the provided password matches the stored plain text password
        if (password == db_password):
            session['user_id'] = result[0]   # Store user ID in session
            session['name'] = result[1]      # Store user name in session
            return 0
        
        #If the password is incorrect
        elif (password != result[2]):
            return 1
        
        #If the Email is not registered
        else:
            return 2
    
    def fetch_name(email):
        conn = Account.create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM users WHERE email = %s', [email])
        retrieve_records = cursor.fetchone()
        retrieve_name = retrieve_records[0]
        return retrieve_name

    def create_account(email, name, password, hp_no, status, profile):
        #Insert user data into database
        conn = Account.create_connection()
        cursor = conn.cursor()
        data = (email, name, password, hp_no, status, profile)
        
        #Insert new entries into the database
        try:
            cursor.execute("""INSERT INTO users (email, name, password, handphone_no, acc_status, profile) 
                           VALUES (%s, %s, %s, %s, %s, %s)""", data)
            conn.commit()
            return 0
        
        #Error handler from the database
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return 1
        
        finally:
            cursor.close()
            conn.close()
    
    def delete_account(email):
        conn = Account.create_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE email = %s", email)
        conn.commit()
        cursor.close()
        conn.close()
        return 'User Deleted'


    def get_all_users():
        conn = Account.create_connection()
        cursor = conn.cursor(dictionary=True)  # Return data as dictionaries
        cursor.execute("SELECT profile, name, email, acc_status FROM users") 
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return users

    
    def search_users(profile_type=None, email=None, name=None, status=None):
        conn = Account.create_connection()
        cursor = conn.cursor(dictionary=True)  # Returns results as dictionaries
        query = "SELECT profile, name, email, acc_status FROM users WHERE 1=1"
        params = []

        # Build query dynamically based on provided parameters
        if profile_type:
            query += " AND profile = %s"
            params.append(profile_type)
        
        if email:
            query += " AND email = %s"
            params.append(email)
        
        if name:
            query += " AND name LIKE %s"
            params.append(f"%{name}%")  # Partial match for name

        if status:
            query += " AND acc_status = %s"
            params.append(status)

        cursor.execute(query, params)
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return users


    def suspend_account(email):
        conn = Account.create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE users SET acc_status = 'suspended' WHERE email = %s", (email,))
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return False
        finally:
            cursor.close()
            conn.close()


    def update_account(email, name, status, profile):
        conn = Account.create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE users SET name = %s, profile = %s, acc_status = %s WHERE email = %s", (name, profile, status, email)) 
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return False
        finally:
            cursor.close()
            conn.close()

    def get_user_by_email(email):
        conn = Account.create_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT profile, name, email, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user
