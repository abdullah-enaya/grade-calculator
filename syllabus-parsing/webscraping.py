import json

from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = "https://student.utm.utoronto.ca/CourseInfo/"
driver.get(url)

with open('sensitive.json', "r") as infile:
    data = infile.read()

sensitive = json.loads(data)

# Use the inspect tool on your browser to obtain these ID's
driver.find_element(By.ID, "username").send_keys(sensitive["username"])
driver.find_element(By.ID, "password").send_keys(sensitive["password"])
driver.find_element(By.NAME, "_eventId_proceed").click()    # submit button

# Waits until we have succesfully logged in and grabs the title

# in situations where you wish to wait for a certain amount of time use:
driver.implicitly_wait(15)

session_field = Select(driver.find_element(By.ID, "session_cd"))
session_field.select_by_value("20241")
driver.implicitly_wait(10)
downloads = driver.find_elements(By.LINK_TEXT, "Download")
for element in downloads:
    element.click()
