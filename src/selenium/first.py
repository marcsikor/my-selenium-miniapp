from selenium import webdriver
from selenium.webdriver.common.by import By

from statistics import mean
import time
import json

with open('credentials.json') as cred:
    credentials_dict = json.load(cred)

with open('portal-paths.json') as paths:
    paths_dict = json.load(paths)

driver = webdriver.Chrome()

driver.get(paths_dict["login-page"]) # login

login = driver.find_element(By.ID, "username")
login_input = credentials_dict["login"]
login.send_keys(login_input)

password = driver.find_element(By.ID, "password")
password_input = credentials_dict["password"]
password.send_keys(password_input)

login_button = driver.find_element(By.NAME, "submitBtn")
login_button.click()

driver.get(paths_dict["grades-page"])

periods = driver.find_elements(By.TAG_NAME, "usos-frame-section")

periods_list = []

for period in periods:
    period_text = period.get_attribute("textContent")
    periods_list.append(period_text)

grades = driver.find_elements(By.XPATH, "//usos-frame-section/table/tbody/tr/td/div/span")

grades_list = []

for grade in grades:
    grade_text = grade.get_attribute("innerText")
    if grade_text != 'ZAL' and grade_text != '(brak ocen)':
        grades_list.append(float(grade_text.replace(',', '.')))

print(mean(grades_list))

driver.quit()
