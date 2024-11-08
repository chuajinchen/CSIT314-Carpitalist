from Account import Account
import mysql.connector

class UAdmin(Account):
    #Constructor for User Admin
    def __init__(self):
        super.__init__()
        self.profile = 'User Admin'

    #Function for user admin to create profiles
       
    def create_profile(profile_type, search_cars="yes", view_cars="yes", list_cars="yes"):
        # Establish a database connection
        conn = Account.create_connection()
        if conn is None:
            print("Failed to connect to database.")
            return "Database connection error"
    
        cursor = conn.cursor()
    
        try:
            # Insert a new profile
            insert_query = """
            INSERT INTO profile (profile_type, search_cars, view_cars, list_cars)
            VALUES (%s, %s, %s, %s)"""
            data = (profile_type, search_cars, view_cars, list_cars)
            cursor.execute(insert_query, data)
        
            # Commit changes to the database
            conn.commit()
        
            print(f"Profile '{profile_type}' created successfully.")
            return "Profile created successfully"
        
        except mysql.connector.Error as err:
            # Handle specific MySQL errors
            if err.errno == 1062:
                print("Error: Profile with this type already exists.")
                return "Profile with this type already exists"
            else:
                print(f"Database Error: {err}")
                return "Failed to create profile"
    
        finally:
            # Close the cursor and connection
            cursor.close()
            conn.close()

            return 'Success'
    
   
    
    #Function for user admin to search for specific profile
    def search_users(profile_type=None, email=None, name=None):
        """
        Searches for users in the database based on profile_type, email, or name.
        Any combination of the parameters can be provided for filtering.
        """
        conn = Account.create_connection()
        cursor = conn.cursor(dictionary=True)  # Returns results as dictionaries
        query = "SELECT profile, name, email FROM users WHERE 1=1"
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

        cursor.execute(query, params)
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return users
    
    #Function for user admin to view profiles
    def viewProfile():
        return 'Profiles'

    #Function for user admin to suspend a profile
    def suspendProfile(profile_type):
         # Establish a database connection
        conn = Account.create_connection()
        if conn is None:
            print("Failed to connect to database.")
            return "Database connection error"
    
        cursor = conn.cursor()
    
        try:
            # Insert a new profile
            insert_query = """UPDATE profile SET search_cars = False ,view_cars = False,list_cars = False  WHERE profile_type = %s"""
            data = (profile_type)
            cursor.execute(insert_query, data)
        
            # Commit changes to the database
            conn.commit()
        
            print(f"Profile '{profile_type}' suspended successfully.")
            return "Profile suspended successfully"
        
        except mysql.connector.Error as err:
            # Handle specific MySQL errors
                print(f"Database Error: {err}")
                return "Failed to suspend profile"
    
        finally:
            # Close the cursor and connection
            cursor.close()
            conn.close()

            return 'Suspended Profile'

       
    
    #Function for user admin to update user profile
    def updateProfile(oldprofile,newprofile,description):
        # Establish a database connection
        conn = Account.create_connection()
        if conn is None:
            print("Failed to connect to database.")
            return "Database connection error"
    
        cursor = conn.cursor()
    
        try:
            # Insert a new profile
            insert_query = """UPDATE profile SET profile_type = %s,description = %s WHERE profile_type = %s"""
            data = (newprofile,description,oldprofile)
            cursor.execute(insert_query, data)
        
            # Commit changes to the database
            conn.commit()
            insert_query = """UPDATE user SET profile = %s WHERE profile = %s"""
            data = (newprofile,oldprofile)
            cursor.execute(insert_query, data)
        
            # Commit changes to the database
            conn.commit()
            print(f"Profile '{newprofile}' update successfully.")
            return "Profile update successfully"
        
        except mysql.connector.Error as err:
            # Handle specific MySQL errors
                print(f"Database Error: {err}")
                return "Failed to update profile"
    
        finally:
            # Close the cursor and connection
            cursor.close()
            conn.close()

            return 'Profile updated'
    
    #Function for user admin to create account
    def createAccount(self):
        #Insert user data into database
        conn = Account.create_connection()
        cursor = conn.cursor()
        data = (self.email, self.name, self.password, self.hp_no, self.status, self.profile)
        
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
    
    #Function for user admin to update account
    def updateAccount():
        return 'Account updated'
    
    #Function for user admin to suspend account
    def suspendAccount():
        return 'Account suspended'
    
    #Function for user admin to search for account
    def searchAccount():
        return 'Account details'
