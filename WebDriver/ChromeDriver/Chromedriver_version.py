import requests
from bs4 import BeautifulSoup  # 雖然這段程式沒有實際使用 BeautifulSoup，可以先忽略它
import platform  # 用來偵測作業系統（Windows / Mac / Linux）
import platform, subprocess  # subprocess 可用來執行系統指令，例如抓 Chrome 版本
import xml.etree.ElementTree as ET  # 這段程式也沒使用 ET，可以忽略
from selenium import webdriver  # Selenium 的 WebDriver 模組
from selenium.webdriver.chrome.service import Service  # 用來指定 chromedriver 路徑
import os, time, json  # 檔案操作、等待時間、JSON 檔讀寫

# 如果是 Windows 系統，載入 COM 模組用來抓取 exe 的版本資訊
if platform.system() == 'Windows':
    from win32com.client import Dispatch
    import pythoncom  

class ChromeDriverForMac:
    def __init__(self, system):
        self.originalPath = os.getcwd()  # 儲存當前目錄位置，之後會切回來
        currentPath = os.path.abspath(__file__)  # 當前檔案絕對路徑
        currentDir = os.path.dirname(currentPath)  # 該檔案所在資料夾
        os.chdir(currentDir)  # 切換到該資料夾，方便後續操作檔案

        # 載入 url.json，讀取下載網址與資源路徑
        with open("url.json") as js:
            self.data = json.load(js)
            print("Data", self.data)

        self.System = system  # 儲存目前系統資訊（如 mac-x64）
        self.download_chromedriver()  # 開始下載對應的 chromedriver zip
        self.extract_zip()  # 解壓縮並設置權限

    def climb_chromedriver_version(self):
        import json
        # 取得符合目前 Chrome 版本的 Chromedriver 版本 URL
        if not os.path.isdir("./TEMP"):
            os.makedirs("./TEMP")
        verList = []
        curVersion = self.get_chrome_version() # 取得當前 Chrome 主版本（例如 "121.0"）
        # 偽造 headers，避免被 Google 拒絕連線（有些網站會封鎖無 UA 的請求）
        heads = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}
        # proxy 設定：若你在內網環境中（如公司封鎖外網），可以透過代理伺服器出去
        proxy={'http': 'http://10.10.10.10:8000', 'https': 'http://10.10.10.10:1212'}
        # 發送請求到 Google Chrome for Testing JSON 版本列表
        response = requests.get(self.data['chromedriver-resourse'], headers= heads)
        with open("./TEMP/download_link.json", mode= "w") as f:
            f.write(response.text)
        with open("./TEMP/download_link.json", mode= "r") as f:
            links = json.load(f)
            for i in range(len(links['versions'])):
                if curVersion in links['versions'][i]['version']:
                    verList.append(links['versions'][i]['version'])
            
        print("爬到的ChromeDriver版本為", verList[-1])
        print(f"{self.data['chromedriver-url']}/{verList[-1]}/{self.System}/chromedriver-{self.System}.zip")
        return f"{self.data['chromedriver-url']}/{verList[-1]}/{self.System}/chromedriver-{self.System}.zip"

    def download_chromedriver(self):
        # 下載 chromedriver zip
        if not os.path.isdir("./TEMP"):
            os.makedirs("./TEMP")
        response = requests.get(self.climb_chromedriver_version())
        with open (f"./TEMP/chromedriver.zip", 'wb') as file:
            file.write(response.content)
        startTime = time.time()
        while True:
            if os.path.isfile(f"./TEMP/chromedriver.zip"):
                break
            else:
                if time.time() - startTime > 60:
                    raise
                else:
                    continue

    def extract_zip(self):
        # 解壓縮下載的 zip，並確認資料夾產生
        import zipfile
        file = zipfile.ZipFile(f"./TEMP/chromedriver.zip")
        file.extractall(path= f"./TEMP/")
        file.close()
        startTime = time.time()
        while True:
            if os.path.isdir(f"./TEMP/chromedriver-{self.System}"):
                break
            else:
                if time.time() - startTime() > 60:
                    raise
                else:
                    continue
        os.chdir(f"./TEMP/chromedriver-{self.System}")
        os.system("xattr -d com.apple.quarantine chromedriver") # 解除 Mac 的防護標籤

    def get_chrome_version(self):
        # 使用 subprocess 執行系統指令抓取 Chrome 版本
        if platform.system() == 'Darwin':  # 检查是否是Mac OS
            cmd = "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version"
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()
            version = output.decode('utf-8').strip()
            version = version[14:19] # 只取主版本號，像 "121.0"
            return version
        else:
            return "Chrome version retrieval is only supported on Mac OS"

    def create_driver(self):
        try:
            options = webdriver.ChromeOptions()
            prefs = {
            'profile.default_content_setting_values':
            {
                'notifications': 2,
            },
            'profile.default_content_settings.popups': 0, 
            "profile.default_content_setting_values.clipboard": 1,
            'download.default_directory': os.path.abspath(''),
            "download.prompt_for_download": False,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False
            }
            options.add_experimental_option('prefs', prefs)
            # options.add_argument('--disable-gpu')
            options.add_argument('--lang=zh-TW')
            # options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--window-size=800x600')
            options.add_argument('--mute-audio')
            # options.add_argument('--start-minimized')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--remote-debugging-port=9222')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-features=InterestCohort')
            options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
            # options.add_argument('--log-level=1')
            #抓出與本機端chrome相同版本的版號
            if self.System in ["win32", "win64"]:
                driverName = "chromedriver.exe"
            else:
                driverName = "chromedriver"
            path = os.path.abspath(driverName) # 抓取目前目錄下的 driver
            print(path)
            os.system(f"chmod +x {path}") # 設定執行權限（Mac 專用）
            # driver = webdriver.Chrome(service= Service(executable_path= f"./TEMP/chromedriver-{self.System}/{driverName}"), options= options)
            driver = webdriver.Chrome(service= Service(executable_path= path, log_output="chromedriver.log"),  options= options)
            # driver = webdriver.Chrome(options= options)
            # ExceptionHandler(msg= "Successfully open browser driver. 成功開啟瀏覽器驅動器", exceptionLevel= "info")
            os.chdir(self.originalPath) # 切回原本目錄
            return driver
        except:
            # ExceptionHandler(msg= "Cannot open browser driver. 無法開啟瀏覽器驅動器", exceptionLevel= "critical")
            pass

class ChromeDriverForWindows:
    def __init__(self, system):
        self.originalPath = os.getcwd()  # 儲存目前執行前的目錄位置
        currentPath = os.path.abspath(__file__)  # 取得目前程式檔案的絕對路徑
        currentDir = os.path.dirname(currentPath)  # 取得目前程式所在的資料夾
        os.chdir(currentDir)  # 切換目錄，讓後續檔案操作都在此目錄中
        with open("url.json") as js: # 讀取 url.json 檔案中的資源網址
            self.data = json.load(js)
            print("Data", self.data)
        self.System = system # 記錄系統名稱（例如 win64）
        self.download_chromedriver() # 下載對應版本的 chromedriver
        self.extract_zip() # 解壓縮該檔案並驗證資料夾是否存在


    def climb_chromedriver_version(self):
        import json
        if not os.path.isdir("./TEMP"): # 若 TEMP 資料夾不存在則建立
            os.makedirs("./TEMP")
        verList = []
        curVersion = self.get_chrome_version() # 取得本機 Chrome 主版本號
        response = requests.get(self.data['chromedriver-resourse']) # 向 Google 要求版本清單 JSON
        with open("./TEMP/download_link.json", mode= "w") as f:
            f.write(response.text)
        with open("./TEMP/download_link.json", mode= "r") as f:
            links = json.load(f)
            for i in range(len(links['versions'])):
                if curVersion in links['versions'][i]['version']: # 若符合主版本就加入清單
                    verList.append(links['versions'][i]['version'])
        print("爬到的ChromeDriver版本為", verList[-1])
        print(f"{self.data['chromedriver-url']}/{verList[-1]}/{self.System}/chromedriver-{self.System}.zip")
        return f"{self.data['chromedriver-url']}/{verList[-1]}/{self.System}/chromedriver-{self.System}.zip"

    def download_chromedriver(self):
        if not os.path.isdir("./TEMP"):
            os.makedirs("./TEMP")
        response = requests.get(self.climb_chromedriver_version()) # 下載 zip 檔
        with open (f"./TEMP/chromedriver.zip", 'wb') as file:
            file.write(response.content)
        startTime = time.time()
        while True:
            if os.path.isfile(f"./TEMP/chromedriver.zip"):
                break
            else:
                if time.time() - startTime > 60: # 若超過 60 秒沒下載成功就丟錯誤
                    raise
                else:
                    continue

    def extract_zip(self):
        import zipfile
        file = zipfile.ZipFile(f"./TEMP/chromedriver.zip") # 解壓縮 zip
        file.extractall(path= f"./TEMP/")
        file.close()
        startTime = time.time()
        while True:
            if os.path.isdir(f"./TEMP/chromedriver-{self.System}"): # 等待資料夾出現
                break
            else:
                if time.time() - startTime() > 60:
                    raise
                else:
                    continue

    def get_version_via_com(self, filename): #從目標路徑取得該機器上的Chrome當前版本
        # 透過 COM 物件取得 Windows 安裝的 Chrome 檔案版本
        pythoncom.CoInitialize()
        parser = Dispatch("Scripting.FileSystemObject")
        try:
            version = parser.GetFileVersion(filename)
        except Exception:
            return None
        print("電腦當前Chrome版本為", version)
        return version

    def get_chrome_version(self): #將機器的chrome版本最後一位去除
        self.chromeVersion = list(filter(None, [self.get_version_via_com(p) for p in [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]]))[0]
        tmp = self.chromeVersion.split(".")
        for i in range(2):
            tmp.pop() # 移除最後兩段版本號
        self.chromeVersion = ".".join(tmp)
        return self.chromeVersion + "." # 回傳形如 "121.0." 的主版本
    
    def create_driver(self):
        try:
            options = webdriver.ChromeOptions()
            prefs = {
            'profile.default_content_setting_values':
            {
                'notifications': 2,
            },
            'profile.default_content_settings.popups': 0, 
            "profile.default_content_setting_values.clipboard": 1,
            'download.default_directory': os.path.abspath(''),
            "download.prompt_for_download": False,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False
            }
            options.add_experimental_option('prefs', prefs)
            # options.add_argument('--disable-gpu')
            options.add_argument('--lang=zh-TW')
            # options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--window-size=800x600')
            options.add_argument('--mute-audio')
            # options.add_argument('--start-minimized')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--remote-debugging-port=9222')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-features=InterestCohort')
            options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
            options.add_argument('--log-level=1')
            #抓出與本機端chrome相同版本的版號
            if self.System in ["win32", "win64"]:
                driverName = "chromedriver.exe"
            else:
                driverName = "chromedriver"
            # path = os.path.abspath(f"./TEMP/chrome/driver-win64/{driverName}")
            # path = os.path(f"./TEMP/chrome/driver-win64/{driverName}")
            # 組合 chromedriver 執行檔完整路徑
            path = os.path.join(os.path.dirname(__file__), f"TEMP/chromedriver-win64/{driverName}")
            print(path)
            # driver = webdriver.Chrome(service= Service(executable_path= f"./TEMP/chromedriver-{self.System}/{driverName}", service_args=["--verbose", "--enable-logging", "--log-level=0" ]), options= options)
            driver = webdriver.Chrome(service= Service(executable_path=path, log_output= "chromedriver.log"), options= options)
            # driver = webdriver.Chrome(service= Service(executable_path= path))
            # ExceptionHandler(msg= "Successfully open browser driver. 成功開啟瀏覽器驅動器", exceptionLevel= "info")
            os.chdir(self.originalPath) # 切回原始目錄
            return driver
        except:
            # ExceptionHandler(msg= "Cannot open browser driver. 無法開啟瀏覽器驅動器", exceptionLevel= "critical")
            pass