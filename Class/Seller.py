from Account import Account
import mysql.connector

class Seller:
    #Constructor for Seller object
    def __init__(self):
        super.__init__()
        self.profile = 'Seller'

    #Functions for seller to look at listing view count
    def viewCount():
        return 'Vehicle Online view count'
    
    #Functions for seller to track shortlist count
    def shortlistCount():
        return 'Vehicle shortlist count'
    
    #Functions for seller to rate used car agent
    def rateUCA():
        return 'Agent rated'
    
    #Functions for seller to review used car agent
    def reviewUCA():
        return 'Agent reviewed'
    
    #Functions for seller to look ratings and review
    def lookRR():
        return 'Agents rating and review'
    
    
