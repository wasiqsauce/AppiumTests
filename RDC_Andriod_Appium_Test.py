#Test Passed on Sauce Labs - Application working properly
import os
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
import time

# Sauce Labs credentials from environment variables
SAUCE_USERNAME = os.environ.get('SAUCE_USERNAME')
SAUCE_ACCESS_KEY = os.environ.get('SAUCE_ACCESS_KEY')

# Check if credentials are set
if not SAUCE_USERNAME or not SAUCE_ACCESS_KEY:
    raise ValueError("SAUCE_USERNAME and SAUCE_ACCESS_KEY environment variables must be set")

# Sauce Labs URL (adjust to eu-central-1 if needed)
SAUCE_URL = f"https://{SAUCE_USERNAME}:{SAUCE_ACCESS_KEY}@ondemand.us-west-1.saucelabs.com:443/wd/hub"


def test_android_app():
    driver = None
    try:
        # Initialize UiAutomator2Options for Android
        options = UiAutomator2Options()
        options.set_capability("platformName", "Android")
        options.set_capability("appium:platformVersion", "13")  # Adjust to match available device version
        options.set_capability("appium:deviceName", "Samsung Galaxy S23 Plus")
        options.set_capability("appium:automationName", "UiAutomator2")
        options.set_capability("appium:app",
                               "storage:filename=Android-MyDemoAppRN.1.3.0.build-244.apk")
        #options.set_capability("appium:appiumVersion", "2.0.0")
        options.set_capability("appium:language","en")
        options.set_capability("appium:locale","US")
        options.set_capability("orientation","PORTRAIT")
        options.set_capability("autoGrantPermissions",True)
        options.set_capability("newCommandTimeout",90)
        options.set_capability("browserName", "")
        # Sauce Labs specific options
        options.set_capability("sauce:options", {
            "name": "Android App Test - RDC",
            "appiumVersion": "stable",
            "sessionCreationRetry": 2,
            "sessionCreationTimeout": 300000,
            "deviceOrientation": "PORTRAIT",
            "imageInjection": True,
            # "tunnelName": "oauth-wasiq.wani-2032a_tunnel_name",
            # "tunnelOwner": "oauth-wasiq.wani-2032a"
        })

        # Initialize the Appium driver
        driver = webdriver.Remote(
            command_executor=SAUCE_URL,
            options=options
        )

        # Wait for the app to load
        time.sleep(5)

        # Example test action: Find an element by accessibility ID and interact
        # Replace 'login_button' with an actual accessibility ID from your app
        login_button = driver.find_element(AppiumBy.XPATH, "(//android.view.ViewGroup[@content-desc='store item'])[1]/android.view.ViewGroup[1]")
        login_button.click()

        # Wait to observe the action
        time.sleep(2)

        # Mark test as passed in Sauce Labs
        driver.execute_script('sauce:job-result=passed')

    except Exception as e:
        # Only mark test as failed if driver was initialized
        if driver:
            driver.execute_script('sauce:job-result=failed')
        print(f"Test failed: {str(e)}")
        raise

    finally:
        # Quit the driver if it was initialized
        if driver:
            driver.quit()


if __name__ == "__main__":
    test_android_app()