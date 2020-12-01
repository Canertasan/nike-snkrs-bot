import pip

def import_or_install(package):
  try:
    __import__(package)
  except ImportError:
    pip.main(['install', package])   


if __name__ == '__main__':
  required_packages = ["selenium", "webdriver_manager"] # required packages
  for package in required_packages:
    import_or_install(package)