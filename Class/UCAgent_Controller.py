from UCAgent import UCAgent

class CreateCarListing:
    def __init__(self, reg_no, brand, make_id, car_type, color, price, mileage, descrip, seller_email, agent_email):
        self.reg_no = reg_no
        self.brand = brand
        self.make_id = make_id
        self.car_type = car_type
        self.color = color
        self.price = price
        self.mileage = mileage
        self.descrip = descrip
        self.seller_email = seller_email
        self.agent_email = agent_email

    def execute(self):
        return UCAgent.create_car_listing(self.reg_no, self.brand, self.make_id, self.car_type,
                                          self.color, self.price, self.mileage, self.descrip,
                                          self.seller_email, self.agent_email)


class DeleteCarListing:
    def __init__(self, reg_no):
        self.reg_no = reg_no

    def execute(self):
        return UCAgent.delete_car_listing(self.reg_no)


class UpdateCarListing:
    def __init__(self, reg_no, price, status, description):
        self.reg_no = reg_no
        self.price = price
        self.status = status
        self.description = description

    def execute(self):
        return UCAgent.update_car_listing(self.reg_no, self.price, self.status, self.description)


class GetCarListings:
    @staticmethod
    def execute():
        return UCAgent.get_car_listings()


class SearchCarListings:
    def __init__(self, make, min_price=None, max_price=None):
        self.make = make
        self.min_price = min_price
        self.max_price = max_price

    def execute(self):
        return UCAgent.search_car_listings(self.make, self.min_price, self.max_price)


class GetReviews:
    def __init__(self, agent_email):
        self.agent_email = agent_email

    def execute(self):
        return UCAgent.get_reviews(self.agent_email)


class GetCarByRegNo:
    def __init__(self, reg_no):
        self.reg_no = reg_no

    def execute(self):
        return UCAgent.get_car_by_reg_no(self.reg_no)


class GetMakeId:
    def __init__(self, make_name):
        self.make_name = make_name

    def execute(self):
        return UCAgent.get_make_id(self.make_name)


class GetEmailByName:
    def __init__(self, agent_name):
        self.agent_name = agent_name

    def execute(self):
        return UCAgent.get_email_by_name(self.agent_name)
