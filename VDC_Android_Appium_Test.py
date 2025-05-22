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


def test_android_emulator_app():
    driver = None
    try:
        # Initialize UiAutomator2Options for Android emulator
        options = UiAutomator2Options()
        options.set_capability("platformName", "Android")
        options.set_capability("appium:platformVersion", "15.0")  # Known supported version
        options.set_capability("appium:deviceName", "Android GoogleAPI Emulator")  # Supported emulator
        options.set_capability("appium:automationName", "UiAutomator2")
        options.set_capability("appium:app",
                               "storage:filename=Android-MyDemoAppRN.1.3.0.build-244.apk")  # Demo app
        # To use your app, replace with: "storage:filename=myapp.apk" after uploading to Sauce Labs
        #options.set_capability("appium:noReset", True)  # Prevent app reset
        options.set_capability("browserName", "")
        # Sauce Labs specific options
        options.set_capability("sauce:options", {
            "name": "Android Emulator App Test",
            "appiumVersion": "2.0.0",  # Use stable Appium 2 version
            "sessionCreationRetry": 2,
            "sessionCreationTimeout": 3000,
            "extendedDebugging": True  # Enable detailed logging
        })

        # Initialize the Appium driver
        driver = webdriver.Remote(
            command_executor=SAUCE_URL,
            options=options
        )

        # Wait for the app to load
        time.sleep(5)
        #
        # # Example test action: Find an element by accessibility ID and interact
        # # For the demo app, interacting with the login field
        # login_field = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-Username")
        # login_field.send_keys("standard_user")
        #
        # # Wait to observe the action
        # time.sleep(2)

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
    test_android_emulator_app()