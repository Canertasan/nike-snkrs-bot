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
import multiprocessing

# Product Info
PRODUCT_URL = "https://www.nike.com/tr/launch/t/kobe-6-protro-green-apple"
RELEASING_TIME = 14

def getProduct(email, password, cvc, shoe_size):
  # Create a driver
  driver = WebDriver()
  # Get product page
  driver.openBrowser(PRODUCT_URL)
  # When time arrives run! 
  driver.waitTime(RELEASING_TIME)
  # Select number and go basket
  driver.selectItem(shoe_size)
  # after select shoe login
  driver.login(email, password)
  # Payment
  driver.payments(cvc)
  print("You are in line!")
  time.sleep(10000) # Don't close browser

if __name__ == '__main__':
  # we should read file for accounts, take email pw, cvc  Yes we should but try first 20 account without reading csv, see result.
  # add proxy do we need proxy?
  shoe_size = "44"
  cvc = "330"
  password = "159753Caner."
  p1 = multiprocessing.Process(target=getProduct, args=("caner.tasan@hotmail.com",password, cvc, shoe_size,))
  p2 = multiprocessing.Process(target=getProduct, args=("canertasan@sabanciuniv.edu",password, cvc, shoe_size,))
  p1.start() # starting workers
  p2.start() # starting workers