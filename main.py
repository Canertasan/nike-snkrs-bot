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
RELEASING_TIME = 14

def getProduct(email, password, cvc, shoe_size, url):
  # Create a driver
  driver = WebDriver()
  # Get product page
  driver.openBrowser(url)
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
  # try this
  PRODUCT_URL_1 = "https://www.nike.com/tr/launch/t/womens-air-jordan-1-zoom-pink-glaze"
  # multiprocessing.Process(target=getProduct, args=("caner.tasan@hotmail.com",password, cvc, "38",PRODUCT_URL_1)).start()
  multiprocessing.Process(target=getProduct, args=("canertasan@sabanciuniv.edu",password, cvc, "38.5",PRODUCT_URL_1)).start()
  multiprocessing.Process(target=getProduct, args=("gulerman36@hotmail.com",password, cvc, "38",PRODUCT_URL_1)).start()
  multiprocessing.Process(target=getProduct, args=("kaansakarca123@hotmail.com",password2, cvc, "39",PRODUCT_URL_1)).start()
  multiprocessing.Process(target=getProduct, args=("resellkc@hotmail.com",password2, cvc, "38",PRODUCT_URL_1)).start()
  multiprocessing.Process(target=getProduct, args=("k.sakarca@gmail.com",password2, cvc, "39",PRODUCT_URL_1)).start()
  multiprocessing.Process(target=getProduct, args=("huseyintasan37@gmail.com",password, cvc, "38.5",PRODUCT_URL_1)).start()
  multiprocessing.Process(target=getProduct, args=("jalesakarca@hotmail.com",password2, cvc, "38.5",PRODUCT_URL_1)).start()

  # PRODUCT_URL_2 = "https://www.nike.com/tr/launch/t/womens-dunk-low-disrupt-copa"
  # multiprocessing.Process(target=getProduct, args=("caner.tasan@hotmail.com",password, cvc, "44",PRODUCT_URL_2)).start()
  # multiprocessing.Process(target=getProduct, args=("canertasan@sabanciuniv.edu",password, cvc, "44.5",PRODUCT_URL_2)).start()
  # multiprocessing.Process(target=getProduct, args=("gulerman36@hotmail.com",password, cvc, "45",PRODUCT_URL_2)).start()
  # multiprocessing.Process(target=getProduct, args=("kaansakarca123@hotmail.com",password2, cvc, "40.5",PRODUCT_URL_2)).start()
  # multiprocessing.Process(target=getProduct, args=("resellkc@hotmail.com",password2, cvc, "40.5",PRODUCT_URL_2)).start()
  # multiprocessing.Process(target=getProduct, args=("k.sakarca@gmail.com",password2, cvc, "44",PRODUCT_URL_2)).start()
  # multiprocessing.Process(target=getProduct, args=("huseyintasan37@gmail.com",password, cvc, "43",PRODUCT_URL_2)).start()
  # multiprocessing.Process(target=getProduct, args=("jalesakarca@hotmail.com",password2, cvc, "44.5",PRODUCT_URL_2)).start()

  # PRODUCT_URL_3 = "https://www.nike.com/tr/launch/t/womens-dunk-low-disrupt-copa"
  # multiprocessing.Process(target=getProduct, args=("caner.tasan@hotmail.com",password, cvc, "44",PRODUCT_URL_3)).start()
  # multiprocessing.Process(target=getProduct, args=("canertasan@sabanciuniv.edu",password, cvc, "44.5",PRODUCT_URL_3)).start()
  # multiprocessing.Process(target=getProduct, args=("gulerman36@hotmail.com",password, cvc, "45",PRODUCT_URL_3)).start()
  # multiprocessing.Process(target=getProduct, args=("kaansakarca123@hotmail.com",password2, cvc, "40.5",PRODUCT_URL_3)).start()
  # multiprocessing.Process(target=getProduct, args=("resellkc@hotmail.com",password2, cvc, "40.5",PRODUCT_URL_3)).start()
  # multiprocessing.Process(target=getProduct, args=("k.sakarca@gmail.com",password2, cvc, "44",PRODUCT_URL_3)).start()
  # multiprocessing.Process(target=getProduct, args=("huseyintasan37@gmail.com",password, cvc, "43",PRODUCT_URL_3)).start()
  # multiprocessing.Process(target=getProduct, args=("jalesakarca@hotmail.com",password2, cvc, "44.5",PRODUCT_URL_3)).start()

