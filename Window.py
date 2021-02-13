from tkinter import *
import threading
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import zipfile
import multiprocessing
import threading
import sys


class WebDriver:
  def __init__(self, proxy_host, proxy_port, proxy_username, proxy_pw, order):
    options = Options()
    self.proxy = proxy_host
    PROXY_HOST = proxy_host # rotating proxy
    PROXY_PORT = proxy_port
    PROXY_USER = proxy_username
    PROXY_PASS = proxy_pw

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
              },
              bypassList: ["localhost"]
            }
          };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

    pluginfile = 'proxy_auth_plugin_%s.zip' % order

    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    options.add_extension(pluginfile)

    # options.add_argument('--headless') # how to find element with headless and how to authenticate with headless to proxy
    # options.add_argument('--disable-gpu') # this is coming with headless
    options.add_argument("disable-infobars")
    self.chrome = webdriver.Chrome(ChromeDriverManager().install(), options=options)

  def accept_terms(self, order):
    try:
      # self.result_label["text"] = "Trying to accepting Terms"
      window.set_result_label_text(order, "Trying to accepting Terms")
      print("accepting terms")
      self.wait_until_clickable(xpath="//button[@class='ncss-btn-primary-dark']",duration=30)
      accept_button = self.chrome.find_element_by_xpath("//button[@class='ncss-btn-primary-dark']")
      accept_button.click()
    except TimeoutException:
      # self.result_label["text"] = "Terms didnt asked"
      print("Does not ask for terms")

  def openBrowser(self, url, order):
    try:
      window.set_result_label_text(order, "Opening Browser")
      print("Opening browser")
      self.chrome.get(url)
    except TimeoutException:
      print("Page load timed out but continuing anyway")

  def wait_until_visible(self, xpath=None, class_name=None, duration=10000, frequency=0.01):
    if xpath:
        WebDriverWait(self.chrome, duration, frequency).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    elif class_name:
        WebDriverWait(self.chrome, duration, frequency).until(EC.visibility_of_element_located((By.CLASS_NAME, class_name)))

  def wait_until_visible_popup(self, xpath=None, class_name=None, duration=10000, frequency=0.01):
    if xpath:
        WebDriverWait(self.chrome, duration, frequency).until(EC.presence_of_element_located((By.XPATH, xpath)))
    elif class_name:
        WebDriverWait(self.chrome, duration, frequency).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))

  def wait_until_clickable(self, xpath=None, class_name=None, duration=10000, frequency=0.01):
    if xpath:
        WebDriverWait(self.chrome, duration, frequency).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    elif class_name:
        WebDriverWait(self.chrome, duration, frequency).until(EC.element_to_be_clickable((By.CLASS_NAME, class_name)))

  def wait_until_frame_to_be_available_and_switch_to_it(self, xpath=None, class_name=None, duration=10000, frequency=0.01):
    if xpath:
      WebDriverWait(self.chrome, duration, frequency).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, xpath)))
    elif class_name:
      WebDriverWait(self.chrome, duration, frequency).until(EC.frame_to_be_available_and_switch_to_it((By.CLASS_NAME, class_name)))

  # def wait_until_execution(self)

  def login(self, email, password, cvc, order):
    try:
      #login first
      self.wait_until_clickable(xpath="//button[text()='Katıl / Oturum Aç' and @class='join-log-in text-color-grey prl3-sm pt2-sm pb2-sm fs12-sm d-sm-b']")
      pop_up_btn = self.chrome.find_element_by_xpath("//button[text()='Katıl / Oturum Aç' and @class='join-log-in text-color-grey prl3-sm pt2-sm pb2-sm fs12-sm d-sm-b']")
      self.chrome.execute_script("arguments[0].click();", pop_up_btn)
      time.sleep(3)

      window.set_result_label_text(order, "Waiting for login fields to become visible")
      print("Waiting for login fields to become visible")
      self.wait_until_visible(xpath="//input[@name='emailAddress']")

      window.set_result_label_text(order, "Entering username and password: "+ email)
      print("Entering username and password:", email)
      email_input = self.chrome.find_element_by_xpath("//input[@name='emailAddress']")
      email_input.clear()
      email_input.send_keys(email)
      time.sleep(2)
      password_input = self.chrome.find_element_by_xpath("//input[@name='password']")
      password_input.clear()
      password_input.send_keys(password)
      window.set_result_label_text(order, "Logging in: "+ email)
      print("Logging in", email)
      time.sleep(3)
      login_btn = self.chrome.find_element_by_xpath("//input[@value='OTURUM AÇ']")
      self.chrome.execute_script("arguments[0].click();", login_btn)
      self.wait_until_visible(xpath="//span[@class='test-name text-color-secondary ml2-sm va-sm-m d-sm-h d-md-ib fs-block']", duration=20)
      window.set_result_label_text(order, "Successfully logged in: "+ email)
      print("Successfully logged in", email)
    except TimeoutException:
      window.set_result_label_text(order, self.proxy+ " does not work try new one")
      print(self.proxy, "does not work try new one")
      file1 = open('failed_login_accounts.txt', 'a')
      file1.write(email + ":" + password + ":" + cvc +  "\n")
      file1.close()
      file2 = open('failed_proxy.txt', 'a')
      file2.write(self.proxy + "\n")
      file2.close()
      self.chrome.close()
      return False
    except:
      window.set_result_label_text(order, "Unexpected error on LOGIN:" + str(sys.exc_info()[0]) + self.proxy)
      print("Unexpected error on LOGIN:", sys.exc_info()[0], self.proxy)
      return False
    return True
      

  # pause.until(date_parser.parse(release_time))
  def waitTime(self, time, order):
    is_it_first_run=True
    window.set_result_label_text(order, "Waiting time...")
    print("Waiting time...")
    while True:
      now = datetime.now()
      if time <= now.hour and not is_it_first_run:
        self.chrome.refresh()
        break
      elif time <= now.hour and is_it_first_run:
        break
      is_it_first_run = False
    window.set_result_label_text(order, "Time arrived.")
    print("Time arrived.")
  
  def selectItem(self, shoe_size, email, password, cvc, order):
    try:
      self.chrome.execute_script("scroll(0, 900)") # for delete devicemotion
      time.sleep(5)
      path = "//button[text()='EU " + shoe_size + "']"
      window.set_result_label_text(order, "Selecting shoe number...: " + shoe_size+  " email: " + email)
      print("Selecting shoe number...:", shoe_size, "email:", email)
      self.wait_until_clickable(xpath=path, duration=30)
      time.sleep(1)
      shoe_num_btn = self.chrome.find_element_by_xpath(path)
      self.chrome.execute_script("arguments[0].click();", shoe_num_btn)
      window.set_result_label_text(order, "Number is selected: " + shoe_size+  " email: " + email)
      print("Number is selected:", shoe_size, "email:", email)
      self.wait_until_clickable(xpath="//button[@class='ncss-btn-primary-dark btn-lg test']")
      time.sleep(1)
      buy_btn = self.chrome.find_element_by_xpath("//button[@class='ncss-btn-primary-dark btn-lg test']")
      self.chrome.execute_script("arguments[0].click();", buy_btn)
      window.set_result_label_text(order, "Shoe number selected: " + shoe_size+  " email: " + email)
      print("Shoe number selected:", shoe_size, "email:", email)
      return True
    except TimeoutException:
      window.set_result_label_text(order, "Numbers cannot loaded yet. Try with new proxy")
      print("Numbers cannot loaded yet. Try with new proxy")
      file1 = open('failed_login_accounts.txt', 'a')
      file1.write(email + ":" + password + ":" + cvc +  "\n")
      file1.close()
      file2 = open('failed_proxy.txt', 'a')
      file2.write(self.proxy + "\n")
      file2.close()
      self.chrome.close()
      return False
    except:
      print("Unexpected error on SELECT ITEM:", sys.exc_info()[0])
      return False

  def payments(self, cvc, shoe_size, email, order):
    try:
      window.set_result_label_text(order, "Paying for the shoe: " + shoe_size+  " email: " + email)
      print("Paying for the shoe:", shoe_size, "email:", email )
      # Need class and name at the same time because it is inside in iframe
      self.wait_until_visible(xpath="//iframe[@title='payment' and @class='cvv']")
      window.set_result_label_text(order, 'iframe finded')
      print('iframe finded')
      iframe = self.chrome.find_element_by_xpath("//iframe[@title='payment' and @class='cvv']")
      self.chrome.switch_to.frame(iframe)
      window.set_result_label_text(order, "iframe switched")
      print("iframe switched")
      self.wait_until_visible(xpath="//input[@name='cardCvc']")
      print("CVC is visible")
      cvc_input = self.chrome.find_element_by_xpath("//input[@name='cardCvc']")
      cvc_input.clear()
      cvc_input.send_keys(cvc)
      time.sleep(1)
      print("CVC filled")
      self.chrome.switch_to.default_content()
      print("switch default content")
      self.chrome.execute_script("scroll(0, 300)") # for seeing buttons
      time.sleep(5)
      print("scroll is done clicking buttons.")
      self.wait_until_clickable(xpath="//button[@type='button' and @class='button-continue']")
      continue_btn = self.chrome.find_element_by_xpath("//button[@type='button' and @class='button-continue']")
      self.chrome.execute_script("arguments[0].click();", continue_btn)
      time.sleep(1)
      print("button clicked")
      submit_btn = self.chrome.find_element_by_class_name('button-submit') #submit
      self.chrome.execute_script("arguments[0].click();", submit_btn)
      window.set_result_label_text(order, "Payment taken: " + shoe_size+  " email: " + email)
      print("Payment taken.", shoe_size, "email:", email)
    except:
      file2 = open('failed_proxy.txt', 'a')
      file2.write(self.proxy + "\n")
      file2.close()
      print("Unexpected error on PAYMENT:", sys.exc_info()[0])

  def wait_pop_up(self, order):
    try:
      self.wait_until_visible_popup(class_name="ncss-col-sm-12 full bg-white ta-sm-r test-modal-close")
    except:
      print("failed to find popup")
      time.sleep(10000)

  def win_or_loose(self, order):
    self.wait_until_visible(xpath="//h3[@class='headline-3']")
    text = self.chrome.find_element_by_xpath("//h3[@class='headline-3']")
    if text == "Alamadınız":
      print("lost")
    else:
      print("win")

# Product Info
RELEASING_TIME = 14
COUNTER = 0

class Window:
  def __init__(self):
    self.window=Tk()
    self.window.title('Snkrs Bot')
    self.window.geometry("900x600+10+10")
    self.start_all_btn = Button(self.window, text ="Start All", command = self.start_all_accounts)
    self.start_all_btn.place(x=800, y=10)
    self.email_labels = []
    self.result_labels = []
    self.reset_buttons = []
    self.process_infos = []
    self.all_proxies_infos = []
    self.threads = []
  
  def start_loop(self):
    self.window.mainloop()
  
  def getProduct(self, email, password, cvc, shoe_size, url, proxy_host, proxy_port, proxy_username, proxy_password, order):
    # Create a driver
    driver = WebDriver(proxy_host, proxy_port ,proxy_username, proxy_password, order)
    # Get product page
    driver.openBrowser(url,order)
    # accepting termss
    driver.accept_terms(order)
    # login first
    res_login = driver.login(email, password, cvc, order)
    # res_login = True
    if res_login == True:
      # When time arrives run! 
      driver.waitTime(RELEASING_TIME, order)
      # Select number and go basket
      res_select_item = driver.selectItem(shoe_size, email, password, cvc, order)
      if res_select_item == True:
        # Payment
        driver.payments(cvc, shoe_size, email, order)
        print("You are in line!")
        driver.wait_pop_up(order)
        # pop up showed up see win or loose
        driver.win_or_loose(order)
    
  def set_result_label_text(self, index, text):
    self.result_labels[index]["text"] = text

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
      reset_btn=Button(self.window, text=str(counter) + ". " + "Reset", fg='black', command =lambda :  self.restart_browser(index))
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
  
    sizes = [["40.5", "38", "38", "38", "38", "38", "38", "38", "38", "38", "38", "38", "38", "38", "38", "38", "38", "38", "38.5","39","40","40.5","43","44","44.5","38","38.5","38","38.5","39","40","40.5","43","44","44.5","38","38.5","38","38.5","39","40","40.5","43","44","44.5","38","38.5","38","38.5","39","40","40.5","43","44","44.5","38","38.5"],
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
        self.threads.append(p)
        p.start()
        counter += 1
        COUNTER += 1
        break

  def restart_browser(self, index):
    global COUNTER
    print("COUNTER:", COUNTER)
    self.set_result_label_text(index, "Resetting...")
    p = threading.Thread(target=self.getProduct, args=(self.process_infos[index][0],self.process_infos[index][1], self.process_infos[index][2], self.process_infos[index][3],
                              self.process_infos[index][4], 
                              self.all_proxies_infos[COUNTER%len(self.all_proxies_infos)][0], self.all_proxies_infos[COUNTER%len(self.all_proxies_infos)][1], 
                              self.all_proxies_infos[COUNTER%len(self.all_proxies_infos)][2], self.all_proxies_infos[COUNTER%len(self.all_proxies_infos)][3], index))
    self.threads.append(p)
    p.start()
    COUNTER += 1


window = Window()
window.start_loop()



