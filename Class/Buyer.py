from Account import Account
import mysql.connector

class Buyer(Account):
    #Constructor for Buyer Account
    def __init__(self):
        super().__init__()
        self.profile = 'Buyer'

    #Functions for buyers to view car listing
    def viewListing():
        return 'Listing'

    #Functions for buyer to search listing
    def searchListing():
        return 'Specific Listing'
    
    #Functions for buyer to shortlist car list
    def saveList():
        return 'Shortlisted'
    
    #Functions for buyer to look at current Listing
    def viewCurrentListing():
        return 'Current Listing'
    
    #Functions for buyer to rate a used car agent
    def rateUCA():
        return 'UCA rated'
    
    #Functions for buyer to review a used car agent
    def reviewUCA():
        return 'UCA reviewed'
    
    #Functions for buyer to look at rating and review for a used car agent
    def lookRR():
        return 'UCA rating and returns'
    
    #Functions for buyer to calculate payment instalment
    def loanCalculator():
        return 'Results'
    
    
