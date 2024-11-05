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
    def updateListing():
        return 'Listing Updated'
    
    #Function for Used Car Agent to view car listing
    def viewListing():
        return 'List of vehicles'
    
    #Function for Used Car Agent to search listing
    def searchListing():
        return 'Searched Vehicles'

    #Function for Used Car Agent to see own reviews
    def seeReview():
        return 'My reviews'
