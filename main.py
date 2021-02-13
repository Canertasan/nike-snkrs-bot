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
import threading

# Product Info
RELEASING_TIME = 14

def getProduct(email, password, cvc, shoe_size, url, proxy_host, proxy_port, proxy_username, proxy_password, order):
  # Create a driver
  driver = WebDriver(proxy_host, proxy_port ,proxy_username, proxy_password, order)
  # Get product page
  driver.openBrowser(url)
  # accepting termss
  driver.accept_terms()
  # login first
  res_login = driver.login(email, password, cvc)
  # res_login = True
  if res_login == True:
    # When time arrives run! 
    driver.waitTime(RELEASING_TIME)
    # Select number and go basket
    res_select_item = driver.selectItem(shoe_size, email, password, cvc)
    if res_select_item == True:
      # Payment
      driver.payments(cvc, shoe_size, email)
      print("You are in line!")
      driver.wait_pop_up()
      # pop up showed up see win or loose
      driver.win_or_loose()


if __name__ == '__main__':
  accounts = []
  # Using readlines()
  file1 = open('accounts.txt', 'r')
  # file1 = open('failed_login_accounts.txt', 'r')
  Lines = file1.readlines()
  count = 0
  # Strips the newline character
  for line in Lines:
    if line != "":
      account = line.strip()
      account = account.split(':')
      accounts.append(account)
      count += 1

  file3 = open('failed_login_accounts.txt', 'w')
  file3.write("")
  file3.close()

  proxies = []
  file2 = open('proxies.txt', 'r')
  Lines = file2.readlines()
  count = 0
  # Strips the newline character
  for line in Lines:
    proxy = line.strip()
    proxy = proxy.split(':')
    proxies.append(proxy)

  product_urls = ["https://www.nike.com/tr/launch/t/dunk-high-ambush-cosmic-fuchsia"]
 
  sizes = [["38","38.5","39", "40","38","38.5","39", "40","38","38.5","39", "40","38","38.5","39", "40","38","38.5","39", "40","38","38.5","39", "40","38","38.5","39", "40","38","38.5","39", "40", "38", "38", "38", "38", "38", "38", "38", "38", "38", "38", "38", "38", "38", "38", "38", "38", "38.5","39","40","40.5","43","44","44.5","38","38.5","38","38.5","39","40","40.5","43","44","44.5","38","38.5","38","38.5","39","40","40.5","43","44","44.5","38","38.5","38","38.5","39","40","40.5","43","44","44.5","38","38.5"],
            ["41","42","43","44","45","44.5","40.5","43","42","44"]]
  #change here for bad proxies
  counter = 0
  for index, url in enumerate(product_urls, start=0):
    for account in accounts:
      threading.Thread(target=getProduct, args=(account[0],account[1],
                            account[2], sizes[index][counter%len(sizes[index])],url, 
                            proxies[counter%len(proxies)][0], proxies[counter%len(proxies)][1], 
                            proxies[counter%len(proxies)][2], proxies[counter%len(proxies)][3], counter)).start()
      counter += 1
      # if counter >= 10:
      #   break
