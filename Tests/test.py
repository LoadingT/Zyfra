import requests


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.req_session = requests.session()

    def login(self):
        res = self.req_session.post('http://127.0.0.0:5000/login',
                                    json={'username': self.login, 'password': self.password})
        print(res.json())

    def do_something(self):
        res = self.req_session.post('http://127.0.0.0:5000/do_something')
        print(res.json())

    def logout(self):
        res = self.req_session.post('http://127.0.0.0:5000/logout')
        print(res.json())


# class Admin(User):
#    def __init__(self, username, password):
#        super().__init__(username, password)


def test():
    usr = User('123', '123')
    admin = User('admin', 'admin')
    all_users = [usr, admin]
    
    Test1(all_users)
    Test2(all_users)
    Test3(all_users)


def Test1(all_users):
    for user in all_users:
        user.login()
        user.do_something()
        user.logout()

def Test2(all_users):
    for user in all_users:
        user.do_something()
        user.login()
        user.logout()

def Test3(all_users):
    for user in all_users:
        user.do_something()
        user.logout()
        user.login()