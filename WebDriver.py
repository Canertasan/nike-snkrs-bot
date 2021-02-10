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
class WebDriver:
  def __init__(self, proxy_host,proxy_port,proxy_username,proxy_pw,order):
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

  def accept_terms(self):
    try:
      self.wait_until_visible(xpath="//button[@class='ncss-btn-primary-dark']",duration=30)
      accept_button = self.chrome.find_element_by_xpath("//button[@class='ncss-btn-primary-dark']")
      accept_button.click()
    except TimeoutException:
      print("Does not ask for terms")

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

  def login(self, username, password):
    try:
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
      self.wait_until_visible(xpath="//span[@class='test-name text-color-secondary ml2-sm va-sm-m d-sm-h d-md-ib fs-block']", duration=20)
      print("Successfully logged in")
    except TimeoutException:
      print(self.proxy, "does not work try new one")
      file1 = open('failed_login_accounts.txt', 'a')
      file1.write(username + ":" + password + "\n")
      file1.close()
      file2 = open('failed_proxy.txt', 'a')
      file2.write(self.proxy + "\n")
      file2.close()
      

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
    try:
      self.chrome.execute_script("scroll(0, 1000)") # for delete devicemotion
      path = "//button[text()='EU " + shoe_size + "']"
      print("Selecting shoe number...")
      self.wait_until_clickable(xpath=path)
      self.chrome.execute_script("scroll(0, 1000)") # for seeing buttons
      self.chrome.find_element_by_xpath(path).click()
      self.wait_until_clickable(xpath="//button[@class='ncss-btn-primary-dark btn-lg test']")
      self.chrome.find_element_by_xpath("//button[@class='ncss-btn-primary-dark btn-lg test']").click()
      print("Shoe number selected.")
    except:
      file2 = open('failed_proxy.txt', 'a')
      file2.write(self.proxy + "\n")
      file2.close()

  def payments(self, cvc):
    try:
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
    except:
      file2 = open('failed_proxy.txt', 'a')
      file2.write(self.proxy + "\n")
      file2.close()

  def wait_pop_up(self):
    try:
      self.wait_until_visible_popup(class_name="ncss-col-sm-12 full bg-white ta-sm-r test-modal-close")
    except:
      print("failed to find popup")
      time.sleep(10000)

  def win_or_loose(self):
    self.wait_until_visible(xpath="//h3[@class='headline-3']")
    text = self.chrome.find_element_by_xpath("//h3[@class='headline-3']")
    if text == "Alamadınız":
      print("lost")
    else:
      print("win")
