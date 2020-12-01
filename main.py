from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
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
PRODUCT_URL = "https://www.nike.com/tr/launch/t/womens-space-hippie-04-this-is-trash-iron-grey"
TIME = 14

# find your profile data like this: chrome://version/ on chrome
# ref_link: https://www.howtogeek.com/255653/how-to-find-your-chrome-profile-folder-on-windows-mac-and-linux/

def getProduct(email, password, cvc):
  # Create a driver
  driver = WebDriver()
  # Get product page
  driver.openBrowser(PRODUCT_URL)
  # Login while on the product page
  driver.login(email, password)
  # When time arrives run! 
  driver.waitTime(TIME)
  # Select number and go basket
  driver.selectItem()
  # Payment
  driver.payments(cvc)

  print("You are in line!")


if __name__ == '__main__':
  # we should read file for accounts, take email pw, cvc and chrome user data folder name which i have in my laptop!
  email = "canertasan@sabanciuniv.edu"
  password = "159753Caner."
  cvc = "330"
  
  getProduct(email, password, cvc)
