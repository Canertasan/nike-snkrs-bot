from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pickle
import sys
import time
from datetime import datetime
from WebDriver import WebDriver 

# Product Info
PRODUCT_URL = "https://www.nike.com/tr/launch/t/air-max-90-lux-bright-crimson"
RELEASING_TIME = 14
SHOE_SIZE = "39"

def getProduct(email, password, cvc):
  # Create a driver
  driver = WebDriver()
  # Get product page
  driver.openBrowser(PRODUCT_URL)
  # Login while on the product page
  driver.login(email, password)
  # When time arrives run! 
  driver.waitTime(RELEASING_TIME)
  # Select number and go basket
  driver.selectItem(SHOE_SIZE)
  # Payment
  driver.payments(cvc)
  print("You are in line!")
  time.sleep(10000) # Don't close browser


if __name__ == '__main__':
  # we should read file for accounts, take email pw, cvc
  # add proxy
  # open 20 threads in the beginning
  email = "caner.tasan@hotmail.com"
  password = "159753Caner."
  cvc = "330"
  
  getProduct(email, password, cvc)