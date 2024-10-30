from Account import Account
import mysql.connector

class UCAgent(Account):
    #Constructor for Used Car Agent
    def __init__(self):
        super().__init__()
        self.profile = 'Used car Agent'

    #Function for Used Car agent to list vehicles for sale
    def createListing():
        return 'Listing'
    
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
    
