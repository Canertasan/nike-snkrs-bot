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
PRODUCT_URL = "https://www.nike.com/tr/launch/t/sb-dunk-low-pro-court-purple1"
RELEASING_TIME = 14

def getProduct(email, password, cvc, shoe_size, proxy):
  # Create a driver
  driver = WebDriver(proxy)
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
  cvc = "330"
  password = "159753Caner."
  password2 = "654321Ops"
  # define multiprocessings
  p1 = multiprocessing.Process(target=getProduct, args=("caner.tasan@hotmail.com",password, cvc, "44"))
  p2 = multiprocessing.Process(target=getProduct, args=("canertasan@sabanciuniv.edu",password, cvc, "43"))
  p3 = multiprocessing.Process(target=getProduct, args=("gulerman36@hotmail.com",password, cvc, "42"))
  p4 = multiprocessing.Process(target=getProduct, args=("kaansakarca123@hotmail.com",password2, cvc, "41"))
  p5 = multiprocessing.Process(target=getProduct, args=("resellkc@hotmail.com",password2, cvc, "40.5"))
  p6 = multiprocessing.Process(target=getProduct, args=("k.sakarca@gmail.com",password2, cvc, "44.5",))
  p7 = multiprocessing.Process(target=getProduct, args=("huseyintasan37@gmail.com",password, cvc, "45")) # add payment method
  # p8 = multiprocessing.Process(target=getProduct, args=("kaansakarca888@gmail.com",password2, cvc, shoe_size,))  # reset password and add phone number
  # p9 = multiprocessing.Process(target=getProduct, args=("jalesakarca@hotmail.com",password2, cvc, shoe_size2,))  # add phone number and add payment method
  # starting workers
  p1.start()
  p2.start()
  p3.start()
  p4.start()
  p5.start()
  p6.start()
  p7.start()
  # p8.start()
  # p9.start() 
