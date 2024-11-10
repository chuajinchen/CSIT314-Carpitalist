from Account import Account
import mysql.connector

class UCAgent(Account):
    # Function for Used Car agent to list vehicles for sale
    def create_car_listing(reg_no, brand, make_id, car_type, color, price, mileage, descrip, seller_email, agent_email):
        conn = Account.create_connection()
        if conn is None:
            print("Failed to connect to the database.")
            return 1

        try:
            cursor = conn.cursor()

            # Insert into the car_list table with agent_email included
            query = """
                INSERT INTO car_list (reg_no, brand, make_id, type, color, price, mileage, descrip, sale_status, viewCount, shortlistCount, seller_email, agent_email)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'available', 0, 0, %s, %s)
            """
            data = (reg_no, brand, make_id, car_type, color, price, mileage, descrip, seller_email, agent_email)
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
    def updateListing():
        return 'Listing Updated'
    
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
    
    @staticmethod
    def search_car_listings(make, min_price, max_price):
        conn = Account.create_connection()
        if conn is None:
            print("Failed to connect to the database.")
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            # Base query
            query = """
                SELECT cl.reg_no, cb.name AS brand, cm.name AS model, cl.type, cl.color, cl.price, cl.mileage, 
                    cl.descrip, cl.sale_status, cl.viewCount, cl.shortlistCount
                FROM car_list cl
                JOIN car_brand cb ON cl.brand = cb.name
                JOIN car_model cm ON cl.make_id = cm.id
                WHERE 1=1
            """
            params = []

            # Add conditions only if values are provided
            if make:
                query += " AND (cb.name LIKE %s OR cl.type LIKE %s)"
                params.extend([f"%{make}%", f"%{make}%"])
            if min_price is not None:
                query += " AND cl.price >= %s"
                params.append(min_price)
            if max_price is not None:
                query += " AND cl.price <= %s"
                params.append(max_price)

            # Append order by clause
            query += " ORDER BY cl.price ASC"

            cursor.execute(query, params)
            car_listings = cursor.fetchall()
            return car_listings if car_listings else []

        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            return []

        finally:
            cursor.close()
            conn.close()

    #Function for Used Car Agent to see own reviews
    def seeReview():
        return 'My reviews'
    
    #Function used for create listing agent
    @staticmethod
    def get_make_id(make_name):
        conn = Account.create_connection()
        if conn is None:
            print("Failed to connect to the database.")
            return None

        try:
            cursor = conn.cursor()
            query = "SELECT id FROM car_model WHERE name = %s"
            cursor.execute(query, (make_name,))
            result = cursor.fetchone()
            return result[0] if result else None

        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            return None

        finally:
            cursor.close()
            conn.close()
