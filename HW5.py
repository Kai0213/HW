from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

chromedriver_path = "./chromedriver.exe"
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service)

#%%
# 滾動範例
driver.get("https://24h.pchome.com.tw/sites/ai")
time.sleep(2)
driver.execute_script("window.scrollTo(0, 3000)")
print('已往下滾動3000像素')
time.sleep(2)
driver.find_element(By.XPATH,"(//div[@class='icon'])[2]").click()
time.sleep(3)

driver.switch_to.frame('video')
time.sleep(3)
print(driver.find_element(By.XPATH,"//title[contains(text(),'YouTube')]").get_attribute('textContent'))
time.sleep(3)
driver.quit()
# %%
