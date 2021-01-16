from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import sys
class WebDriver:
  def __init__(self, proxy):
    # options = webdriver.ChromeOptions()
    # user_agent = 'Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
    # webdriver.DesiredCapabilities.CHROME['proxy'] = {
    #   "httpProxy": proxy,
    #   "ftpProxy": proxy,
    #   "sslProxy": proxy,
    #   "proxyType": "MANUAL",
    # }
    # options.add_argument("user-agent="+user_agent)
    # options.add_argument('--proxy-server=%s' % proxy)
    # webdriver.DesiredCapabilities.CHROME['acceptSslCerts']=True
    # print(webdriver.DesiredCapabilities.CHROME)
    # self.chrome = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    # TRY FIRST WITHOUT PROXY
    self.chrome = webdriver.Chrome(ChromeDriverManager().install())


  def openBrowser(self, url):
    try:
      print("Requesting page: " + url)
      self.chrome.get(url)
    except TimeoutException:
      print("Page load timed out but continuing anyway")

  def wait_until_visible(self, xpath=None, class_name=None, duration=10000, frequency=0.01):
    if xpath:
        WebDriverWait(self.chrome, duration, frequency).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    elif class_name:
        WebDriverWait(self.chrome, duration, frequency).until(EC.visibility_of_element_located((By.CLASS_NAME, class_name)))

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

  def login(self, username, password):
    print("Waiting for login fields to become visible")
    self.wait_until_visible(xpath="//input[@name='emailAddress']")

    print("Entering username and password")
    email_input = self.chrome.find_element_by_xpath("//input[@name='emailAddress']")
    email_input.clear()
    email_input.send_keys(username)
    password_input = self.chrome.find_element_by_xpath("//input[@name='password']")
    password_input.clear()
    password_input.send_keys(password)
    print("Logging in")
    self.chrome.find_element_by_xpath("//input[@value='OTURUM AÇ']").click()
    self.wait_until_visible(xpath="//span[@class='test-name text-color-secondary ml2-sm va-sm-m d-sm-h d-md-ib fs-block']")
    print("Successfully logged in")

  # pause.until(date_parser.parse(release_time))
  def waitTime(self, time):
    is_it_first_run=True
    print("Waiting time...")
    while True:
      now = datetime.now()
      if time <= now.hour and not is_it_first_run:
        self.chrome.refresh()
        break
      elif time <= now.hour and is_it_first_run:
        break
      is_it_first_run = False
    print("Time arrived.")
  
  def selectItem(self, shoe_size):
    self.chrome.execute_script("scroll(0, 1000)") # for delete devicemotion
    path = "//button[text()='EU " + shoe_size + "']"
    print("Selecting shoe number...")
    self.wait_until_clickable(xpath=path)
    self.chrome.execute_script("scroll(0, 1000)") # for seeing buttons
    self.chrome.find_element_by_xpath(path).click()
    self.wait_until_clickable(xpath="//button[@class='ncss-btn-primary-dark btn-lg test']")
    self.chrome.find_element_by_xpath("//button[@class='ncss-btn-primary-dark btn-lg test']").click()
    print("Shoe number selected.")

  def payments(self, cvc):
    print("Paying for the shoe.")
    # Need class and name at the same time because it is inside in iframe
    self.wait_until_visible(xpath="//iframe[@title='payment' and @class='cvv']")
    print('iframe finded')
    iframe = self.chrome.find_element_by_xpath("//iframe[@title='payment' and @class='cvv']")
    self.chrome.switch_to.frame(iframe)
    print("iframe switched")
    self.wait_until_visible(xpath="//input[@name='cardCvc']")
    print("CVC is visible")
    cvc_input = self.chrome.find_element_by_xpath("//input[@name='cardCvc']")
    cvc_input.clear()
    cvc_input.send_keys(cvc)
    print("CVC filled")
    self.chrome.switch_to.default_content()
    print("switch default content")
    self.chrome.execute_script("scroll(0, 300)") # for seeing buttons
    print("scroll is done clicking buttons.")
    self.wait_until_clickable(xpath="//button[@type='button' and @class='button-continue']")
    self.chrome.find_element_by_xpath("//button[@type='button' and @class='button-continue']").click()
    time.sleep(1)
    print("button clicked")
    self.chrome.find_element_by_class_name('button-submit').click() #submit
    print("Payment taken.")
