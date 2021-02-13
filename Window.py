from tkinter import *
from WebDriver import WebDriver 
import threading

# Product Info
RELEASING_TIME = 14
COUNTER = 0

class Window:
  def __init__(self):
    self.window=Tk()
    self.window.title('Snkrs Bot')
    self.window.geometry("900x600+10+10")
    self.start_all_btn = Button(self.window, text ="Start All", command = self.start_all_accounts)
    self.start_all_btn.pack(side=RIGHT)
    self.email_labels = []
    self.result_labels = []
    self.reset_buttons = []
    self.process_infos = []
    self.all_proxies_infos = []
    self.process = []
  
  def start_loop(self):
    self.window.mainloop()
  
  def getProduct(self, email, password, cvc, shoe_size, url, proxy_host, proxy_port, proxy_username, proxy_password, order):
    # Create a driver
    driver = WebDriver(proxy_host, proxy_port ,proxy_username, proxy_password, order)
    # Get product page
    driver.openBrowser(url)
    # accepting termss
    driver.accept_terms()
    # login first
    # res_login = driver.login(email, password, cvc)
    res_login = True
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

  def start_all_accounts(self):
    cvc = "330"
    accounts = []
    # Using readlines()
    file1 = open('accounts.txt', 'r')
    # file1 = open('failed_login_accounts.txt', 'r')
    Lines = file1.readlines()
    counter = 0
    # Strips the newline character
    for line in Lines:
      index = counter
      account = line.strip()
      account = account.split(':')
      accounts.append(account)
      email=Label(self.window, text=str(counter) + ". " + account[0], fg='black', font=("Helvetica", 12))
      email.place(x=10, y=(10 + counter*30))
      self.email_labels.append(email)
      result=Label(self.window, text="Status: " + "starting...", fg='black', font=("Helvetica", 12))
      result.place(x=250, y=(10 + counter*30))
      self.result_labels.append(result)
      reset_btn=Button(self.window, text=str(counter) + ". " + "Reset", fg='black', font=("Helvetica", 12), command =lambda :  self.restart_browser(index))
      reset_btn.place(x=600, y=(10 + counter*30))
      self.reset_buttons.append(reset_btn)
      counter+=1

    file2 = open('proxies.txt', 'r')
    Lines = file2.readlines()
    # Strips the newline character
    for line in Lines:
      proxy = line.strip()
      proxy = proxy.split(':')
      self.all_proxies_infos.append(proxy)

    product_urls = ["https://www.nike.com/tr/launch/t/womens-lahar-low-wheat"]
  
    sizes = [["38", "38", "38", "38", "38", "38", "38", "38", "38", "38", "38", "38", "38", "38", "38", "38", "38", "38", "38.5","39","40","40.5","43","44","44.5","38","38.5","38","38.5","39","40","40.5","43","44","44.5","38","38.5","38","38.5","39","40","40.5","43","44","44.5","38","38.5","38","38.5","39","40","40.5","43","44","44.5","38","38.5"],
            ["41","42","43","44","45","44.5","40.5","43","42","44"]]
    counter = 0
    global COUNTER
    for index, url in enumerate(product_urls, start=0):
      for account in accounts:
        infos = [account[0],account[1], cvc, sizes[index][counter%len(sizes[index])],url]
        self.process_infos.append(infos)
        p = threading.Thread(target=self.getProduct, args=(account[0],account[1], cvc, sizes[index][counter%len(sizes[index])],url, 
                              self.all_proxies_infos[counter%len(self.all_proxies_infos)][0], self.all_proxies_infos[counter%len(self.all_proxies_infos)][1], 
                              self.all_proxies_infos[counter%len(self.all_proxies_infos)][2], self.all_proxies_infos[counter%len(self.all_proxies_infos)][3], counter))
        self.process.append(p)
        p.start()
        counter += 1
        COUNTER += 1

  def restart_browser(self, index):
    global COUNTER
    print("COUNTER:", COUNTER)
    p = threading.Thread(target=self.getProduct, args=(self.process_infos[index][0],self.process_infos[index][1], self.process_infos[index][2], self.process_infos[index][3],
                              self.process_infos[index][4], 
                              self.all_proxies_infos[COUNTER%len(self.all_proxies_infos)][0], self.all_proxies_infos[COUNTER%len(self.all_proxies_infos)][1], 
                              self.all_proxies_infos[COUNTER%len(self.all_proxies_infos)][2], self.all_proxies_infos[COUNTER%len(self.all_proxies_infos)][3], COUNTER))
    self.process.append(p)
    p.start()
    COUNTER += 1


if __name__ == '__main__':
  window = Window()
  window.start_loop()
