#The username and password is not input in the test on Sauce Labs
import os
import random
import string
from appium.webdriver.webdriver import WebDriver
from appium.options.common.base import AppiumOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Sauce Labs credentials from environment variables
sauce_username = os.getenv('SAUCE_USERNAME')
sauce_access_key = os.getenv('SAUCE_ACCESS_KEY')
sauce_url = 'https://ondemand.us-west-1.saucelabs.com/wd/hub'

# Set up Appium options for Android emulator on Sauce Labs
options = AppiumOptions()
options.set_capability('platformName', 'Android')
options.set_capability('appium:platformVersion', '15.0')
options.set_capability('appium:deviceName', 'Android GoogleAPI Emulator')
options.set_capability('appium:automationName', 'UiAutomator2')
options.set_capability('browserName', 'Chrome')
options.set_capability('sauce:options', {
    'username': sauce_username,
    'accessKey': sauce_access_key,
    "appiumVersion": "2.0.0",
    'name': 'SauceDemo Web App test VDC - Appium',
    'build': 'Python-Appium-SauceDemo-Test'
})


# Initialize the remote WebDriver
driver = WebDriver(command_executor=sauce_url, options=options)

try:
    # Navigate to saucedemo.com
    driver.get('https://www.saucedemo.com')

    driver.execute_script('sauce:job-result=passed')

finally:
    # Clean up and quit the driver
    driver.quit()