import os
import cv2
import pyautogui
import numpy as np
import gc
import shutil
from PIL import ImageGrab, ImageEnhance

class SystemAction:
    def create_folder(self, path, folder_name): # 建立指定資料夾，若不存在才會建立
        if not os.path.exists(f"./{path}/{folder_name}"):
            os.makedirs(f"./{path}/{folder_name}")
    def delete_folder(self, path, folder_name):
        # while os.path.exists(f"./{path}/{folder_name}"):
        #     try:
        #         shutil.rmtree(f"./{path}/{folder_name}") 
        #     except:
        #         continue 
        try:
            shutil.rmtree(f"./{path}/{folder_name}")
        except:
            print("目錄不存在")

    def delete_file(self, path, file_name):
        if os.path.exists(f"./{path}/{file_name}"):
            os.remove(f"./{path}/{file_name}")
    
    def image_compare(self, src_img, tar_img):
        # 比較兩張圖片的差異，回傳 MSE (均方誤差)
        src = cv2.imread(src_img)
        tar = cv2.imread(tar_img)
        
        img1 = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        img2 = cv2.cvtColor(tar, cv2.COLOR_BGR2GRAY)
        
        diff = cv2.subtract(img1, img2)
        err = np.sum(diff**2)
        mse = err / float(src.shape[0] * src.shape[1])
    
        return float(mse)

    def loading_btn_screen_shot(self, region, save_path="./jvd_gemini_automation/test_pics"):
        # 對畫面指定區域截圖（灰階處理），預設存放路徑
        import datetime, os, time
        if not os.path.isdir(save_path):
            os.mkdir(save_path)
            time.sleep(1)
        time_now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        # screen_shot = pyautogui.screenshot(region=region)
        screen_shot = ImageGrab.grab(bbox=region)
        gray_image = screen_shot.convert("L")
        # screen_shot.save(f"{save_path}/{time_now}.png")
        gray_image.save(f"{save_path}/{time_now}.png", icc_profile=None)
        time.sleep(2)

    def case_screen_shot(self, region, save_path, gray, blur, whitetext):
        # 測試截圖處理，支援轉灰階、白字反顯、模糊處理
        import datetime, os, time
        if not os.path.isdir(save_path):
            os.mkdir(save_path)
            time.sleep(1)
        time_now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        # screen_shot = pyautogui.screenshot(region=region)
        screen_shot = ImageGrab.grab(bbox=region)
        if gray:
            gray_image = screen_shot.convert("L")
        # screen_shot.save(f"{save_path}/{time_now}.png")
            gray_image.save(f"{save_path}/{time_now}.png", icc_profile=None)
        else:
            screen_shot.save(f"{save_path}/{time_now}.png", icc_profile=None)
        time.sleep(2)
        if whitetext:
            image = cv2.imread(f"{save_path}/{time_now}.png")
            # height, width = image.shape[:2]
            # image = cv2.resize(image, (width//2, height//2))
            
            # 轉換為灰度圖
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # 設置閾值，將白色文字分離出來
            # 假設白色文字的像素值接近 255
            _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
            
            # 創建一個全黑的背景
            black_background = np.zeros_like(image)
            
            # 將白色文字部分複製到黑色背景上
            # 找出白色區域的像素
            white_text = cv2.bitwise_and(image, image, mask=binary)
            blurred = cv2.GaussianBlur(white_text, (5,5), 0)
            
            output_path = f"{save_path}/{time_now}.png"
            # 將結果保存
            if blur:
                cv2.imwrite(output_path, blurred)
            else:
                cv2.imwrite(output_path, white_text)

        # if not os.path.isdir(save_path):
        #     os.mkdir(save_path)
        #     time.sleep(1)
        # time_now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        # screen_shot = ImageGrab.grab(bbox=region)
        # screen_shot = screen_shot.convert("RGB")
        # width, height = screen_shot.size
        # pixels = screen_shot.load()
        # WHITE_THRESHOLD = 220

        # for x in range(width):
        #     for y in range(height):
        #         r, g, b = pixels[x, y]
        #         if r < WHITE_THRESHOLD or g < WHITE_THRESHOLD or b < WHITE_THRESHOLD:
        #             pixels[x, y] = (70, 70, 70)
        #         else:
        #             pixels[x, y] = (255, 255, 255)
        # # screen_shot.show()
        # # enhancer = ImageEnhance.Contrast(gray_image)
        # # enhanced_image = enhancer.enhance(3.0)
        # # enhanced_image.show()
        # screen_shot.save(f"{save_path}/{time_now}.png", icc_profile=None)
        # time.sleep(2)


    def get_words_from_image(self, image_path, text_threshold=0.5, threshold=0.2, mag_ratio=3.0, low_text=0.3, min_size=5, allowlist="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,.:_ "):
        # 使用 EasyOCR 擷取圖片中的文字，支援參數調整與白名單
        import easyocr
        reader = easyocr.Reader(['en'], gpu=False)
        result = reader.readtext(image = image_path, allowlist=allowlist, 
                                text_threshold=text_threshold, threshold= threshold,mag_ratio=mag_ratio, low_text=low_text, min_size=min_size)
        result_list = []
        for de in result:
            result_list.append(de[1].upper())
        print(result_list)
        return result_list

    def clear_data(self):
        # 清除測試圖片與 chromedriver TEMP 資料夾
        SystemAction().delete_folder("jvd_gemini_automation", "test_pics")
        SystemAction().delete_folder("jvd_gemini_automation/WebDriver/ChromeDriver", "TEMP")
        gc.collect()

    def clear_chromedriver(self):
        # 單獨清除 chromedriver TEMP 資料夾
        SystemAction().delete_folder("jvd_gemini_automation/WebDriver/ChromeDriver", "TEMP")


    def clear_screen_shots(self):
        # 單獨清除 test_pics 資料夾
        SystemAction().delete_folder("jvd_gemini_automation", "test_pics")
        gc.collect()