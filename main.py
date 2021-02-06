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

def getProduct(email, password, cvc, shoe_size, url, proxy_host, proxy_port, proxy_username, proxy_password, order):
  # Create a driver
  driver = WebDriver(proxy_host, proxy_port ,proxy_username, proxy_password, order)
  # Get product page
  driver.openBrowser(url)
  # accepting terms
  driver.accept_terms()
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
  accounts = []
  # Using readlines()
  file1 = open('accounts.txt', 'r')
  Lines = file1.readlines()
  count = 0
  # Strips the newline character
  for line in Lines:
    account = line.strip()
    account = account.split(':')
    accounts.append(account)

  proxies = []
  file2 = open('proxies.txt', 'r')
  Lines = file2.readlines()
  count = 0
  # Strips the newline character
  for line in Lines:
    proxy = line.strip()
    proxy = proxy.split(':')
    proxies.append(proxy)

  product_urls = ["https://www.nike.com/tr/launch/t/air-max-90-deep-royal-blue"]
 
  sizes = [["38","38.5","39","38","38.5","39","38","38.5","38","38.5"],
          ["38","38.5","39","38","38.5","39","38","38.5","38","38.5"]]
  counter = 0
  for index, url in enumerate(product_urls, start=0):
    for account in accounts:
      multiprocessing.Process(target=getProduct, args=(account[0],account[1],
                            cvc, sizes[index][counter%len(sizes[index])],url, 
                            proxies[counter%len(proxies)][0], proxies[counter%len(proxies)][1], 
                            proxies[counter%len(proxies)][2], proxies[counter%len(proxies)][3], counter)).start()
      counter += 1
  
