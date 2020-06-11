__author__ = 'itay.mizeretz'


class User(object):
    def __init__(self, user_id, username, secret):
        self.id = user_id
        self.username = username
        self.secret = secret

    def __str__(self):
        return "User(id='%s')" % self.id
