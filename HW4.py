from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chromedriver_path = "./chromedriver.exe"
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service)

driver.get("https://24h.pchome.com.tw/")
time.sleep(5)

try:
    if (driver.find_element(By.XPATH,"//button[@aria-label='close button']").is_displayed() == True):
        print("出現廣告. 點擊關閉鍵...")
        driver.find_element(By.XPATH,"//button[@aria-label='close button']").click()
except:
    print("未出現廣告, 繼續執行腳本...")


def action_1():
    while True:
        keyword = input('請輸入手機商品關鍵字: ')
        
        # 預先清除輸入框的數字
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='search']"))
        )
        search_input.clear()
        
        # 輸入文字到輸入框並搜索
        search_input.send_keys(keyword)
        search_input.send_keys(Keys.ENTER)
        time.sleep(2)
        
        try:
            # 嘗試選擇手機/平板分類
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//div[text()='手機/平板']"))
            ).click()
            time.sleep(1)
            
            # 選擇手機
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//div[text()='手機']"))
            ).click()
            time.sleep(1)
            
            return keyword
        
        except Exception as e:
            print('無法搜尋到手機/平板相關資訊，請重新輸入關鍵字')

def action_2(keyword):
    while True:
        try:
            sort_method = int(input('請輸入數字: 1:推薦排行、2:新上架、3:價格 : '))
            if sort_method in [1, 2, 3]:
                break
            else:
                print('請輸入數字 1, 2, 3')
        except ValueError:
            print("輸入無效，請輸入一個整數。")
    
    sort_methods = {
        1: ('推薦排行', '//span[text()="推薦排行" and @class="btn__text"]'),
        2: ('新上架', '//span[text()="新上架" and @class="btn__text"]'),
        3: ('價格', '//span[text()="價格" and @class="btn__text"]')
    }
    
    sort_method_str, xpath = sort_methods[sort_method]
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    ).click()
    time.sleep(2)
    
    lowerPrice = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "(//div[@class='c-prodInfoV2__priceValue c-prodInfoV2__priceValue--m'])[1]"))
    ).text
    goodsName = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='c-prodInfoV2__title'][1]"))
    ).text
    
    print(f'搜索關鍵字: {keyword}')
    print(f'依據{sort_method_str}排序結果:')
    print(f'搜尋結果:第一個商品名稱: "{goodsName}"\n第一個商品價格: "{lowerPrice}"')

def main():
    keyword = action_1()
    if keyword:
        action_2(keyword)
    driver.quit()

if __name__ == "__main__":
    main()
