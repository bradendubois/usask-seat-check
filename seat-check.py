from datetime import datetime
from json import loads
from pathlib import Path
from time import sleep

import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.relative_locator import locate_with

paws_root = "http://paws5.usask.ca/"
banner_root = "https://banner.usask.ca/StudentRegistrationSsb/ssb/term/termSelection?mode=search"

data = loads(Path("./data.json").read_text())

driver = webdriver.Chrome()
driver.get(paws_root)

def post(state):
    current = datetime.now()
    date = f"{current.year}:{current.month}:{current.day}"
    time = f"{current.hour}:{current.minute}:{current.second}"
    message = state["message"]
    requests.post(
        state["hook"],
        json={"content": f"**{date}** : {time} : {message}"},
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    )


while True:

    try:        

        driver.implicitly_wait(0.5)
        sleep(1)

        if "Sign in - University of Saskatchewan" in driver.title:

            print(f"In login : {driver.title}")

            username = driver.find_element(By.ID, "username")
            password = driver.find_element(By.ID, "password")
            sign_in = driver.find_element(locate_with(By.TAG_NAME, "input").below({By.ID: "password"}))

            username.send_keys(data["username"])
            password.send_keys(data["password"])
            sign_in.click()

        elif "Remember Device" in driver.title:

            print(f"MFA Page : {driver.title}")

            remember =  driver.find_element(locate_with(By.XPATH, "//*[contains(@value, 'Yes, Remember this device')]"))
            remember.click()

        elif "PAWS - University of Saskatchewan" in driver.title:

            # successful sign-in : can jump right to Banner search without navigating through menus
            driver.get(banner_root)

        elif "Select a Term" in driver.title:

            remember =  driver.find_element(locate_with(By.XPATH, "//*[contains(@class, 'select2-choice select2-default')]"))
            remember.click()

            driver.implicitly_wait(0.5)

            enter = driver.find_element(locate_with(By.ID, "s2id_autogen1_search"))
            enter.send_keys("2022 Fall Term", Keys.RETURN)

            driver.implicitly_wait(1)
            sleep(2)
            enter.send_keys(Keys.RETURN)
            sleep(1)
            
            continue_ = driver.find_element(locate_with(By.ID, "term-go"))
            continue_.click()

        elif "Class Search" in driver.title:

            subject =  driver.find_element(locate_with(By.ID, "s2id_autogen1"))            
            subject.click()

            driver.implicitly_wait(0.5)

            subject.send_keys(data["subject"], Keys.RETURN)
            driver.implicitly_wait(1)
            sleep(2)
            subject.send_keys(Keys.RETURN)
            sleep(1)

            course = driver.find_element(locate_with(By.ID, "txt_courseNumber"))
            course.send_keys(data["course"], Keys.RETURN)

            driver.implicitly_wait(1)
            sleep(2)

            any_available = False
            for idx in range(len(driver.find_elements(locate_with(By.XPATH, "//table/tbody/tr")))):
                row = driver.find_element(locate_with(By.XPATH, f"//table/tbody/tr[{idx+1}]/td[10]"))
                for attr in row.get_property('attributes'):
                    name, value = attr['name'], attr['value']

                    if name != "title":
                        continue

                    numbers = [int(s) for s in value.split() if s.isdigit()]
                    available = numbers[0]

                    if available > 0:
                        any_available = True                        

            post(data["available"] if any_available else data["full"])

            sleep(5)
            driver.refresh()

        else:            
            print(f"unknown: {driver.title}")
            driver.get(banner_root)
            post(data["broken"])

    except Exception as e:
        post(data["broken"])
        driver.get(banner_root)
        continue
