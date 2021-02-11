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
from tkinter import *

# Product Info
RELEASING_TIME = 14

def getProduct(email, password, cvc, shoe_size, url, proxy_host, proxy_port, proxy_username, proxy_password, order):
  # Create a driver
  driver = WebDriver(proxy_host, proxy_port ,proxy_username, proxy_password, order)
  # Get product page
  driver.openBrowser(url)
  # accepting terms
  driver.accept_terms()
  #login first
  driver.login(email, password)
   # When time arrives run! 
  driver.waitTime(RELEASING_TIME)
  # Select number and go basket
  driver.selectItem(shoe_size)
  # Payment
  driver.payments(cvc)
  print("You are in line!")
  driver.wait_pop_up()
  # pop up showed up see win or loose
  driver.win_or_loose()


if __name__ == '__main__':
  # window=Tk()
  # window.title('Snkrs Bot')
  # window.geometry("800x500+10+10")
  
  cvc = "330"
  accounts = []
  # Using readlines()
  file1 = open('accounts.txt', 'r')
  # file1 = open('failed_login_accounts.txt', 'r')
  Lines = file1.readlines()
  count = 0
  # Strips the newline character
  for line in Lines:
    account = line.strip()
    account = account.split(':')
    accounts.append(account)

  file3 = open('failed_login_accounts.txt', 'a')
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

  product_urls = ["https://www.nike.com/tr/launch/t/womens-air-jordan-1-silver-toe"]
 
  sizes = [["38","38.5","39","38","38.5","39","38","38.5","38","38.5"],
            ["41","42","43","44","45","44.5","40.5","43","42","44"]]
  counter = 0
  for index, url in enumerate(product_urls, start=0):
    for account in accounts:
      # email=Label(window, text=str(counter) + ". " + account[0], fg='black', font=("Helvetica", 14))
      # email.place(x=10, y=(10 + counter*10))
      # result=Label(window, text="Status: " + "starting...", fg='black', font=("Helvetica", 14))
      # result.place(x=250, y=(10 + counter*10))
      multiprocessing.Process(target=getProduct, args=(account[0],account[1],
                            cvc, sizes[index][counter%len(sizes[index])],url, 
                            proxies[counter%len(proxies)][0], proxies[counter%len(proxies)][1], 
                            proxies[counter%len(proxies)][2], proxies[counter%len(proxies)][3], counter)).start()
      counter += 1
  # window.mainloop()
  
