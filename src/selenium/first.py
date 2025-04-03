from selenium import webdriver
from selenium.webdriver.common.by import By

from statistics import mean
import json

with open('credentials.json') as cred:
    credentials_dict = json.load(cred)

with open('portal-paths.json') as paths:
    paths_dict = json.load(paths)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

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

periods_dict = {}
grades_list = []

periods = driver.find_elements(By.TAG_NAME, "usos-frame-section")

for period in periods:
    period_text = period.get_attribute("section-title")
    grades = period.find_elements(By.XPATH, ".//table/tbody/tr/td/div/span")
    
    for grade in grades:
        grade_text = grade.get_attribute("innerText")
        if grade_text != 'ZAL' and grade_text != '(brak ocen)':
            grades_list.append(float(grade_text.replace(',', '.'))) 
    
    if len(grades_list) != 0:
        periods_dict[period_text] = mean(grades_list)
    else:
        periods_dict[period_text] = 0.0
    grades_list.clear()

with open('output.json', 'w') as f:
    json.dump(periods_dict, f)
driver.quit()
