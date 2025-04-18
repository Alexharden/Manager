from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
import pyautogui, time, os

class WebAction:
    def __init__(self):
        self.driver: webdriver.Chrome
        self.action: ActionChains
        self.pyat = pyautogui

    def wait_element(self, element, timeout=20):
        WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((By.XPATH, element)))
    
    def wait_elements(self, elements, timeout=20):
        WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located((By.XPATH, elements)))
    def wait_element_visible(self, element, timeout=20):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, element)))
            return True
        except TimeoutException:
            return False
    def find_element(self, element):
        self.wait_element(element)
        return self.driver.find_element(By.XPATH, element)

    def find_elements(self, elements):
        self.wait_elements(elements)
        return self.driver.find_elements(By.XPATH, elements)

    def element_click(self, webElement: WebElement):
        webElement.click()

    def mouse_click(self, position):
        time.sleep(2)
        position = list(position)
        self.pyat.click(x=position[0], y=position[1], duration=0.5)
        time.sleep(2)

    def send_value(self, webElement: WebElement, value):
        webElement.send_keys(value)
        
    def click_by_xpath(self, xpath: str):
        """傳入 xpath 字串，自動找元素並點擊"""
        self.find_element(xpath).click()

    def send_keys_by_xpath(self, xpath: str, value: str):
        """傳入 xpath 與 value，自動找元素並輸入文字"""
        self.find_element(xpath).send_keys(value)

    def close_web(self):
        try:
            if self.driver is not None:
                self.driver.quit()
        except Exception as e:
            print(f"關閉 WebDriver 時發生錯誤 {e}")
        finally:
            self.driver=None

    def element_shot(self, element: WebElement):
        import datetime
        time_now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        element.screenshot(f"./jvd_gemini_automation/test_pics/{time_now}.png")
        time.sleep(3)