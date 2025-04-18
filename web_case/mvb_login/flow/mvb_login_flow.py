from web_case.mvb_login.uit.mvb_login_uit import *
class LoginFlow():
    def __init__(self, uit:LoginUit):
        self.uit = uit
    def input_account(self):
        self.uit.send_account()
    def click_next_button(self):
        self.uit.click_next()
    def input_password(self):
        self.uit.send_passwrod()
    def click_sigin(self):
        self.uit.click_sigin()

class MvbLoginFlow:
    def __init__(self, uit:MvbLoginUit):
        self.uit = uit
        self.__login = LoginFlow(self.uit.login)
    @property
    def login(self): return self.__login