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
PRODUCT_URL = "https://www.nike.com/tr/launch/t/air-jordan-1-volt-gold1"
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
  # we should read file for accounts, take email pw, cvc  Yes we should but try first 20 account without reading csv, see result.
  # add proxy do we need proxy?
  shoe_size = "44"
  shoe_size2 = "40.5"
  cvc = "330"
  password = "159753Caner."
  password2 = "654321Ops"
  # define multiprocessings
  p1 = multiprocessing.Process(target=getProduct, args=("caner.tasan@hotmail.com",password, cvc, shoe_size, "103.146.176.124:80"))
  # p2 = multiprocessing.Process(target=getProduct, args=("canertasan@sabanciuniv.edu",password, cvc, shoe_size,))
  p3 = multiprocessing.Process(target=getProduct, args=("gulerman36@hotmail.com",password, cvc, shoe_size, "173.46.67.172:58517"))  # does this payment method added save my credit cart?
  p4 = multiprocessing.Process(target=getProduct, args=("kaansakarca123@hotmail.com",password2, cvc, shoe_size2, "43.224.10.42:6666"))
  p5 = multiprocessing.Process(target=getProduct, args=("resellkc@hotmail.com",password2, cvc, shoe_size2, "37.49.127.231:8080"))
  p6 = multiprocessing.Process(target=getProduct, args=("k.sakarca@gmail.com",password2, cvc, shoe_size2, "37.49.127.238:8080"))
  # p7 = multiprocessing.Process(target=getProduct, args=("resellkc@hotmail.com",password2, cvc, shoe_size,))
  # p8 = multiprocessing.Process(target=getProduct, args=("kaansakarca888@gmail.com",password2, cvc, shoe_size,))
  # p9 = multiprocessing.Process(target=getProduct, args=("k.sakarca@gmail.com",password2, cvc, shoe_size,))
  # starting workers
  p1.start()
  # p2.start()
  p3.start()
  p4.start()
  p5.start()
  p6.start()
  # p7.start()
  # p8.start()
  # p9.start() 