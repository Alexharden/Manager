from base_driver.web_action import WebAction
from web_case.mvb_login.element.mvb_login_element import *

class LoginUit():
    def __init__(self, element:LoginToManagerElement):
        self.element = element
        self.driver =WebAction()
    def send_account(self):
        self.driver.send_keys_by_xpath(self.element.account_input)
    def click_next(self):
        self.driver.click_by_xpath(self.element.next_button_element)
    def send_passwrod(self):
        self.driver.send_keys_by_xpath(self.element.password_inputbox_element)
    def click_sigin(self):
        self.driver.click_by_xpath(self.element.sign_in_button_element)

class MvbLoginUit():
    def __init__(self, element:MvbLoginElement):
        self.__login = LoginUit(element.login)
    @property
    def login(self): return self.__login   