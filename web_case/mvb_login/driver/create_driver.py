from base_driver.web_action import WebAction
from base_driver.system_action import SystemAction
from WebDriver.ChromeDriver.Chromedriver_version import ChromeDriverForMac,ChromeDriverForWindows
import platform

class WebAction(WebAction):
    def __init__(self, url):
        super().__init__()
        if platform.system()=="Windows":
            self.driver = ChromeDriverForWindows("win64").create_driver()
        elif platform.system()=="Darwin":
            self.driver = ChromeDriverForMac("mac-arm64").create_driver()
        self.driver.get(url)
        self.driver.set_window_position(1920, -400)
        self.driver.maximize_window()

class SystemAction(SystemAction):
    def case_screen_shot(self, region, gray, blur, whitetext):
        super().case_screen_shot(region, "./jvd_gemini_automation/test_pics/",gray, blur, whitetext)