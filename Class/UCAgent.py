from Account import Account
import mysql.connector

class UCAgent(Account):
    #Constructor for Used Car Agent
    def init(self):
        super().init()
        self.profile = 'Used car Agent'

    #Function for Used Car agent to list vehicles for sale
    def create_car_listing(reg_no, brand, model, car_type, color, price, mileage, descrip, email):
        conn = Account.create_connection()
        if conn is None:
            print("Failed to connect to the database.")
            return 1

        try:
            cursor = conn.cursor()

            # Fetch the make_id for the given model
            cursor.execute("SELECT id FROM car_model WHERE name = %s", (model,))
            make_id_row = cursor.fetchone()
            if not make_id_row:
                print("Model not found in the car_model table.")
                return 1  # Model not found

            make_id = make_id_row[0]

            # Now insert into the car_list table
            query = """
                INSERT INTO car_list (reg_no, brand, make_id, type, color, price, mileage, descrip, email)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            data = (reg_no, brand, make_id, car_type, color, price, mileage, descrip, email)
            cursor.execute(query, data)
            conn.commit()

            print("Car listing created successfully!")
            return 0  # Success

        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            return 1  # Failure

        finally:
            cursor.close()
            conn.close()

    
    #Function for Used Car Agent to delete listed vehicles
    def deleteListing():
        return 'Deleted'
    
    #Function for Used Car Agent to update listed vehicles info
    
    # Function to update car listing details
    @staticmethod
    def update_car_listing(reg_no, price, status, description):
        conn = Account.create_connection()
        if conn is None:
            print("Failed to connect to the database.")
            return 1

        try:
            cursor = conn.cursor()
            query = "UPDATE car_list SET price = %s, sale_status = %s, descrip = %s WHERE reg_no = %s"
            cursor.execute(query, (price, status, description, reg_no))
            conn.commit()
            print("Car listing updated successfully!")
            return 0  # Success

        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            return 1  # Failure

        finally:
            cursor.close()
            conn.close()
    
    #Function for Used Car Agent to view car listing
    @staticmethod
    def get_car_listings():
        conn = Account.create_connection()
        if conn is None:
            print("Failed to connect to the database.")
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT reg_no, brand, type, color, price, mileage, descrip, sale_status, viewCount, shortlistCount
                FROM car_list
                ORDER BY id DESC
                LIMIT 30
            """
            cursor.execute(query)
            car_listings = cursor.fetchall()  # Fetch up to 30 car listings
            return car_listings

        except Error as e:
            print(f"Database error: {e}")
            return None

        finally:
            cursor.close()
            conn.close()
    
    #Function for Used Car Agent to search listing
    def searchListing():
        return 'Searched Vehicles'

    #Function for Used Car Agent to see own reviews
    def seeReview():
        return 'My reviews'
    
    # Function to get car details by registration number
    @staticmethod
    def get_car_by_reg_no(reg_no):
        conn = Account.create_connection()
        if conn is None:
            print("Failed to connect to the database.")
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT reg_no, brand, type, color, price, mileage, descrip, sale_status FROM car_list WHERE reg_no = %s"
            cursor.execute(query, (reg_no,))
            car_details = cursor.fetchone()  # Fetch the car details
            return car_details

        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            return None

        finally:
            cursor.close()
            conn.close()
