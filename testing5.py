import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Update the path to the Microsoft Edge WebDriver
PATH=  'C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe'
driver = webdriver.Edge(PATH)
driver.get("http://127.0.0.1:8000/login/")
driver.maximize_window()
driver.find_element(By.ID, "email").send_keys("analy@gmail.com")
driver.find_element(By.ID, "pass").send_keys("1234")
driver.find_element(By.ID, "submit").click()


driver.find_element(By.ID, "approved_qs").click()
driver.find_element(By.ID, "5").click()

driver.find_element(By.ID, "message").send_keys("anamika")

driver.find_element(By.ID, "chat_submit").click()
driver.find_element(By.ID, "approved_qs").click()



expectedurl="http://127.0.0.1:8000/approved_qs/"
currenturl=driver.current_url
if expectedurl == currenturl:
    print("Test Case Passed for chatting")
else:
    print("Failed")