from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_id, username, passwd, acc_type):
        self.user_id = user_id
        self.username = username
        self.passwd = passwd
        self.acc_type = acc_type

    def get_id(self):
        return str(self.user_id)