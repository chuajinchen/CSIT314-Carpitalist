from flask import session
from Account import Account  # Make sure to import your Account class from the correct module

class VerifyLogin:
    def __init__(self, profile_type, email, password):
        self.profile_type = profile_type
        self.email = email
        self.password = password

    def execute(self):
        return Account.verify_login(self.profile_type, self.email, self.password)


class FetchName:
    def __init__(self, email):
        self.email = email

    def execute(self):
        return Account.fetch_name(self.email)


class CreateAccount:
    def __init__(self, email, name, password, hp_no, status, profile):
        self.email = email
        self.name = name
        self.password = password
        self.hp_no = hp_no
        self.status = status
        self.profile = profile

    def execute(self):
        return Account.create_account(self.email, self.name, self.password, self.hp_no, self.status, self.profile)


class DeleteAccount:
    def __init__(self, email):
        self.email = email

    def execute(self):
        return Account.delete_account(self.email)


class GetAllUsers:
    @staticmethod
    def execute():
        return Account.get_all_users()


class SearchUsers:
    def __init__(self, profile_type=None, email=None, name=None, status=None):
        self.profile_type = profile_type
        self.email = email
        self.name = name
        self.status = status 

    def execute(self):
        return Account.search_users(self.profile_type, self.email, self.name, self.status)  


class SuspendAccount:
    def __init__(self, email):
        self.email = email

    def execute(self):
        return Account.suspend_account(self.email)


class UpdateAccount:
    def __init__(self, email, name, status, profile):
        self.email = email
        self.name = name
        self.status = status
        self.profile = profile

    def execute(self):
        return Account.update_account(self.email, self.name, self.profile, self.status)


class GetUserByEmail:
    def __init__(self, email):
        self.email = email

    def execute(self):
        return Account.get_user_by_email(self.email)
