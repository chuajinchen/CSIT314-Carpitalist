from Account import Account
import mysql.connector

class Buyer(Account):
    # Static method to retrieve car listings for buyers
    @staticmethod
    def get_available_car_listings():
        conn = Account.create_connection()
        if conn is None:
            print("Failed to connect to the database.")
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT reg_no, brand, type, color, price, mileage, descrip, sale_status, viewCount, shortlistCount, seller_email
                FROM car_list
                WHERE sale_status = 'available'
                ORDER BY id DESC
                LIMIT 30
            """
            cursor.execute(query)
            car_listings = cursor.fetchall()
            return car_listings

        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            return None

        finally:
            cursor.close()
            conn.close()

    # Static method to search car listings based on filters
    @staticmethod
    def search_car_listings(make=None, model=None, min_price=None, max_price=None, max_mileage=None):
        conn = Account.create_connection()
        if conn is None:
            print("Failed to connect to the database.")
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT cl.id, cl.reg_no, cl.brand, cl.type, cl.color, cl.price, cl.mileage, cl.descrip, 
                    cl.sale_status, cl.viewCount, cl.shortlistCount, cl.seller_email
                FROM car_list cl
                JOIN car_brand cb ON cl.brand = cb.name
                JOIN car_model cm ON cl.make_id = cm.id
                WHERE cl.sale_status = 'available'
            """
            params = []

            if make:
                query += " AND cb.name LIKE %s"
                params.append(f"%{make}%")
            if model:
                query += " AND cm.name LIKE %s"
                params.append(f"%{model}%")
            if min_price is not None:
                query += " AND cl.price >= %s"
                params.append(min_price)
            if max_price is not None:
                query += " AND cl.price <= %s"
                params.append(max_price)
            if max_mileage is not None:
                query += " AND cl.mileage <= %s"
                params.append(max_mileage)

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


    # Method to add car to shortlist
    @staticmethod
    def add_to_shortlist(buyer_email, reg_no):
        conn = Account.create_connection()
        if conn is None:
            print("Failed to connect to the database.")
            return None

        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO shortlist (buyer_email, reg_no)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE reg_no = reg_no
            """
            cursor.execute(query, (buyer_email, reg_no))
            conn.commit()
            print(f"Added {reg_no} to shortlist for {buyer_email}")

        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            cursor.close()
            conn.close()


    # Method to get shortlisted cars
    @staticmethod
    def get_shortlist(buyer_email):
        conn = Account.create_connection()
        if conn is None:
            print("Failed to connect to the database.")
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT id, buyer_email, reg_no, added_on
                FROM shortlist
                WHERE buyer_email = %s
            """
            cursor.execute(query, (buyer_email,))
            shortlisted_cars = cursor.fetchall()
            print("Shortlisted Cars:", shortlisted_cars)  # Debug print to verify data
            return shortlisted_cars if shortlisted_cars else []

        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            cursor.close()
            conn.close()


    @staticmethod
    def get_email_by_name(agent_name):
        conn = Account.create_connection()
        if conn is None:
            print("Failed to connect to the database.")
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT email 
                FROM users 
                WHERE name = %s 
                LIMIT 1
            """
            cursor.execute(query, (agent_name,))
            result = cursor.fetchone()  # Fetch the agent's email
            return result['email'] if result else None

        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            return None

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_agent_reviews():
        conn = Account.create_connection()
        if conn is None:
            print("Failed to connect to the database.")
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT agent_email, agent, rating, descript FROM review_list ORDER BY id DESC"
            cursor.execute(query)
            reviews = cursor.fetchall()
            return reviews if reviews else []

        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            return []

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def submit_review(agent_email, rating, descript):
        conn = Account.create_connection()
        if conn is None:
            print("Failed to connect to the database.")
            return None

        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO review_list (agent_email, agent, rating, descript)
                VALUES (%s, %s, %s, %s)
            """
            agent_name = Buyer.get_name_by_email(agent_email)
            cursor.execute(query, (agent_email, agent_name, rating, descript))
            conn.commit()
            print(f"Review added for {agent_name} ({agent_email})")

        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_name_by_email(agent_email):
        conn = Account.create_connection()
        if conn is None:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT name FROM users WHERE email = %s", (agent_email,))
            result = cursor.fetchone()
            return result['name'] if result else None

        finally:
            cursor.close()
            conn.close()
