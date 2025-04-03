from selenium import webdriver
from selenium.webdriver.common.by import By

from statistics import mean

class Scraper:
    def __init__(self, is_headless):       
        # set web driver (is_headless is a boolean switch)
        if is_headless: 
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            self.driver = webdriver.Chrome(options=options)
        else:
            self.driver = webdriver.Chrome()
    
    def execute_login(self, login, password, login_path):
        # get login page
        self.driver.get(login_path)
        
        # enter username
        login_element = self.driver.find_element(By.ID, "username")
        login_element.send_keys(login)
        
        # enter password
        password_element = self.driver.find_element(By.ID, "password")
        password_element.send_keys(password)

        # log in
        login_button = self.driver.find_element(By.NAME, "submitBtn")
        login_button.click()

    def get_grades(self, grades_path):
        # declare empty dict to store output, list for storing grades per semester
        semesters_dict = {}
        grades_list = []
        
        # get grades page
        self.driver.get(grades_path)

        # get semester elements
        semesters = self.driver.find_elements(By.TAG_NAME, "usos-frame-section")

        # iterate through semesters
        for semester in semesters:
            # get semester name
            semester_name = semester.get_attribute("section-title")
            # get grade elements inside current semester element
            grades = semester.find_elements(By.XPATH, ".//table/tbody/tr/td/div/span")
            
            # iterate through grade elements in current semester
            for grade in grades:
                # get grade
                grade_text = grade.get_attribute("innerText")
                # check if grade exists and is a number
                if grade_text != 'ZAL' and grade_text != '(brak ocen)':
                    # cast grade to numeric and append to current grades list
                    grades_list.append(float(grade_text.replace(',', '.')))
            
            # check if there are any grades in current semester
            if len(grades_list) != 0:
                # add to dict - current semester as key, mean of grades list as value
                semesters_dict[semester_name] = mean(grades_list)
            else:
                # if no grades are present for current semester, enter 0.0 
                semesters_dict[semester_name] = 0.0
            
            # clear grades_list before calculating next semester
            grades_list.clear()

        # return semesters' grade averages as a dictionary
        return semesters_dict

    def __del__(self):
        self.driver.quit()
