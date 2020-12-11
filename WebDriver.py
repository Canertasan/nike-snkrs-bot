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
  def __init__(self):
    # options = webdriver.ChromeOptions()
    # options.add_argument("--disable-web-security")
    # options.add_argument("--allow-running-insecure-content")
    # options.add_argument("--incognito")
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument("user-agent=whatever you want")
    # options.add_argument("user-data-dir=/Users/caner/Library/Application Support/Google/Chrome")
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
    # If this is first login the you should uncomment those in below
    # print("Waiting for login button to become clickable")
    # self.wait_until_clickable(xpath="//button[text()='Katıl / Oturum Aç']")
    # self.chrome.find_element_by_xpath("//button[text()='Katıl / Oturum Aç']").click()

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

    #The devicemotion events are blocked by feature policy. See https://github.com/WICG/feature-policy/blob/master/features.md#sensor-features
  
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
    # self.wait_until_frame_to_be_available_and_switch_to_it(xpath="//iframe[@title='payment' and @_ngcontent-smj-c85='')]")
    self.wait_until_frame_to_be_available_and_switch_to_it(xpath="//iframe[@class='cvv')]")
    # iframes = self.chrome.find_element_by_tag_name("iframe")
    print('iframe finded')
    self.chrome.switch_to.frame(self.chrome.find_element_by_xpath("//iframe[@class='cvv')]"))
    # self.chrome.switch_to.frame(iframes[1])
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
    self.wait_until_clickable(xpath="//button[@class='button button-continue']")
    self.chrome.find_element_by_xpath("//button[@class='button button-continue']").click()
    self.wait_until_clickable(xpath="//button[@class='button button-submit']")
    self.chrome.find_element_by_xpath("//button[@class='button button-submit']").click()
    print("Payment taken.")


############ Thread Example ############# 
# from threading import Thread, Lock

# mutex = Lock()
# reached = False


# def runProcess(self):
#     # Make the tests...
#     check = True
#     global reached
#     while check:
#         try:
#             if reached:
#                 self.chrome.close()
#                 return
#             self.chrome.execute_script("""
#             let btn = Array.from(document.querySelectorAll('button.size-grid-dropdown.size-grid-button')).find(el => el.textContent === 'EU 44');
#             btn.click();
#             let btnPayment = document.querySelector("button.cta-btn.u-uppercase.cta-btn.ncss-btn.text-color-white.ncss-brand.d-sm-b.d-lg-ib.pr5-sm.pl5-sm.pt3-sm.pb3-sm.d-sm-ib.bg-black.test-buyable.buyable-full-width.buyable-full-width");
#             btnPayment.click();
#             """)
#             # finish in here
#             check = False
#         except Exception as ex:
#             time.sleep(0.5)
#             self.chrome.refresh()
#             ex_type, ex_value, ex_traceback = sys.exc_info()
#             print("Exception message : %s - hala 1. aşamayi gecemedi" % ex_value)

#     check = True
#     while check:
#         try:
#             if reached:
#                 self.chrome.close()
#                 return
#             self.chrome.execute_script("""
#                 let setInputtedVar = document.querySelector("input#cardCvc-input.form-control.ng-untouched.ng-pristine.ng-invalid")
#                 setInputtedVar.value = "330"
#                 let btn = document.querySelector("button.button-continue")
#                 btn.click()
#                 let btnSubmit = document.querySelector("button.button-submit")
#                 btnSubmit.click()""")
#             # finish in here
#             check = False
#             mutex.acquire()
#             reached = True
#             mutex.release()
#             print("REACHED")
#             self.chrome.maximize_window()
#         except Exception as ex:
#             time.sleep(0.25)
#             ex_type, ex_value, ex_traceback = sys.exc_info()
#             print("Exception message : %s - hala 2. aşamayi gecemedi" % ex_value)


# exitFlag = 0


# class myThread (Thread):
#     def _init_(self, threadID, name, counter, arg):
#         Thread._init_(self)
#         self.threadID = threadID
#         self.name = name
#         self.counter = counter
#         options = Options()
#         options.add_argument(arg)
#         self.chrome = webdriver.Chrome(
#             executable_path="C:/Users/Caner.Tasan/Desktop/scriptTrial/chromedriver83.exe", options=options)
#         # self.chrome.get('https://www.nike.com/tr/launch')

#     def run(self):
#         self.chrome.get(
#             'https://www.nike.com/tr/launch/t/air-max-90-pink-foam')
#         print("Starting " + self.name)
#         runProcess(self)
#         print("Exiting " + self.name)


# # Create new threads
# thread1 = myThread(
#     1, "Thread-1", 1, "user-data-dir=C:/Users/Caner.Tasan/AppData/Local/Google/Chrome/User Data1/")
# thread2 = myThread(
#     2, "Thread-2", 2, "user-data-dir=C:/Users/Caner.Tasan/AppData/Local/Google/Chrome/User Data2/")
# thread3 = myThread(
#     3, "Thread-3", 3, "user-data-dir=C:/Users/Caner.Tasan/AppData/Local/Google/Chrome/User Data3/")
# thread4 = myThread(
#     4, "Thread-4", 4, "user-data-dir=C:/Users/Caner.Tasan/AppData/Local/Google/Chrome/User Data4/")

# # Start new Threads
# thread1.start()
# time.sleep(0.35)
# thread2.start()
# time.sleep(0.35)
# thread3.start()
# time.sleep(0.35)
# thread4.start()
