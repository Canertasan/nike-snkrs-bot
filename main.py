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
PRODUCT_URL = "https://www.nike.com/tr/launch/t/sb-dunk-high-pro-invert"
RELEASING_TIME = 14

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
  driver.selectItem()
  # Payment
  driver.payments(cvc)

  print("You are in line!")


if __name__ == '__main__':
  # we should read file for accounts, take email pw, cvc
  # add proxy
  # open thread 20 times
  email = "caner.tasan@hotmail.com"
  password = "159753Caner."
  cvc = "330"
  
  getProduct(email, password, cvc)