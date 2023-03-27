from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import re
from selenium.common.exceptions import WebDriverException

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


o = webdriver.ChromeOptions()
o.add_argument = {'user-data-dir':'C:\\Users\\Umbreon\\AppData\\Local\\Google\\Chrome\\User Data\\'}

driver = webdriver.Chrome()

avitoLink = "https://www.avito.ma/fr/casablanca/appartements-%C3%A0_louer?o="

propetiesLinks = []

for i in range(1,50) :
    driver.get(avitoLink+str(i))
    properties = driver.find_elements(By.CLASS_NAME,"jejop8-0")
    time.sleep(1)

    for elem in properties :
        link = elem.find_element(By.CLASS_NAME,"jejop8-1").get_attribute('href')
        propetiesLinks.append(link)

price = "sc-1g3sn3w-13"
isBoutique = "jKnRUs"