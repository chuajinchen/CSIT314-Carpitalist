from flask import session
from Seller import Seller

class SubmitReview:
    def __init__(self, agent_email, rating, descript):
        self.agent_email = agent_email
        self.rating = rating
        self.descript = descript

    def execute(self):
        return Seller.submit_review(self.agent_email, self.rating, self.descript)


class GetEmailByName:
    def __init__(self, seller_name):
        self.seller_name = seller_name

    def execute(self):
        return Seller.get_email_by_name(self.seller_name)


class GetCarViewsAndShortlists:
    def __init__(self, seller_email):
        self.seller_email = seller_email

    def execute(self):
        return Seller.get_car_views_and_shortlists(self.seller_email)
