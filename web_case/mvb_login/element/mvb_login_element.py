class LoginToManagerElement():
    @property
    def account_input(self):
        return "//div/input[@name='account'][@placeholder='Account']"
    @property
    def next_button_element(self):
        return "//div/button[@type='button']/span[@data-i18n='auth_btn_next']"
    @property
    def password_inputbox_element(self):
        return "//div/div/input[@type='password']"
    @property
    def sign_in_button_element(self):
        return "//div/button[@type='submit']/span[@data-i18n='auth_sign_in']"


class MvbLoginElement():
    def __init__(self): #driver 要不要加
        self.__login = LoginToManagerElement()
    @property
    def login(self): return self.__login   
