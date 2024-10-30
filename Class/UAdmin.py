from Account import Account
import mysql.connector

class UAdmin(Account):
    #Constructor for User Admin
    def __init__(self):
        super.__init__()
        self.profile = 'User Admin'

    #Function for user admin to create profiles
    def createProfile():
        return 'Success'
    
    #Function for user admin to view profiles
    def viewProfile():
        return 'Profiles'
    
    #Function for user admin to search for specific profile
    def searchProfile():
        return 'Selected Profile'
    
    #Function for user admin to suspend a profile
    def suspendProfile():
        return 'Suspended Profile'
    
    #Function for user admin to update user profile
    def updateProfile():
        return 'Profile updated'
    
    #Function for user admin to create account
    def createAccount():
        return 'Account Created'
    
    #Function for user admin to update account
    def updateAccount():
        return 'Account updated'
    
    #Function for user admin to suspend account
    def suspendAccount():
        return 'Account suspended'
    
    #Function for user admin to search for account
    def searchAccount():
        return 'Account details'
