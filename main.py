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
  # driver.login(email, password)  -> I am not sure first login is the best way.
  # When time arrives run! 
  driver.waitTime(RELEASING_TIME)
  # Select number and go basket
  driver.selectItem(SHOE_SIZE)
  # after select shoe login
  driver.login(email, password)  # Try after login!
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

#   I don't know why but i encounter this issue in only payment part. I execute script with other pages but i didn't get this error.

#     def payments(self, cvc):
#         print("Paying for the shoe.")
#         self.chrome.execute_script("scroll(0, 300)") # for seeing buttons
#         # Need class and name at the same time because it is inside in iframe
#         self.wait_until_visible(xpath="//input[@class='pre-search-input headline-5' and @name='cardCvc']")
#         cvc_input = self.chrome.find_element_by_xpath("//input[@class='pre-search-input headline-5' and @name='cardCvc']")
#         cvc_input.clear()
#         cvc_input.send_keys(cvc)
#         self.wait_until_clickable(xpath="//button[@class='button button-continue']")
#         self.chrome.find_element_by_xpath("//button[@class='button button-continue']").click()
#         self.wait_until_clickable(xpath="//button[@class='button button-submit']")
#         self.chrome.find_element_by_xpath("//button[@class='button button-submit']").click()
#         print("Payment taken.")
    
# This is my code that does not running. Before that error I encountered with another error like this: `Refused to load the script 'http because it violates the following Content Security Policy directive with ChromeDriver Chrome headless Selenium.`

# [I solved this error with this][1]: `self.chrome.execute_cdp_cmd("Page.setBypassCSP", {"enabled": True}) #  to disable Contect Security Policy`


#   [1]: https://stackoverflow.com/questions/59207838/refused-to-load-the-script-because-it-violates-the-following-content-security-po
