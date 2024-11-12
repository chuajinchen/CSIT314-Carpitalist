from flask import session
from Buyer import Buyer

class GetAvailableCarListings:
    @staticmethod
    def execute():
        return Buyer.get_available_car_listings()

class SearchCarListings:
    def __init__(self, make=None, model=None, min_price=None, max_price=None, max_mileage=None):
        self.make = make
        self.model = model
        self.min_price = min_price
        self.max_price = max_price
        self.max_mileage = max_mileage

    def execute(self):
        return Buyer.search_car_listings(self.make, self.model, self.min_price, self.max_price, self.max_mileage)

class AddToShortlist:
    def __init__(self, buyer_email, reg_no):
        self.buyer_email = buyer_email
        self.reg_no = reg_no

    def execute(self):
        return Buyer.add_to_shortlist(self.buyer_email, self.reg_no)

class GetShortlist:
    def __init__(self, buyer_email):
        self.buyer_email = buyer_email

    def execute(self):
        return Buyer.get_shortlist(self.buyer_email)

class GetEmailByName:
    def __init__(self, agent_name):
        self.agent_name = agent_name

    def execute(self):
        return Buyer.get_email_by_name(self.agent_name)

class GetAgentReviews:
    @staticmethod
    def execute():
        return Buyer.get_agent_reviews()

class SubmitReview:
    def __init__(self, agent_email, rating, descript):
        self.agent_email = agent_email
        self.rating = rating
        self.descript = descript

    def execute(self):
        return Buyer.submit_review(self.agent_email, self.rating, self.descript)

class GetNameByEmail:
    def __init__(self, agent_email):
        self.agent_email = agent_email

    def execute(self):
        return Buyer.get_name_by_email(self.agent_email)
