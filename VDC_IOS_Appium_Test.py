import os
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.ios import XCUITestOptions
import time

# Sauce Labs credentials from environment variables
SAUCE_USERNAME = os.environ.get('SAUCE_USERNAME')
SAUCE_ACCESS_KEY = os.environ.get('SAUCE_ACCESS_KEY')

# Check if credentials are set
if not SAUCE_USERNAME or not SAUCE_ACCESS_KEY:
    raise ValueError("SAUCE_USERNAME and SAUCE_ACCESS_KEY environment variables must be set")

# Sauce Labs URL (adjust to eu-central-1 if needed)
SAUCE_URL = f"https://{SAUCE_USERNAME}:{SAUCE_ACCESS_KEY}@ondemand.us-west-1.saucelabs.com:443/wd/hub"


def test_ios_simulator_app():
    driver = None
    try:
        # Initialize XCUITestOptions for iOS simulator
        options = XCUITestOptions()
        options.set_capability("platformName", "iOS")
        options.set_capability("appium:platformVersion", "current_major")  # Known supported version
        options.set_capability("appium:deviceName", "iPhone Simulator")  # Known supported simulator
        options.set_capability("appium:automationName", "XCUITest")
        options.set_capability("appium:app",
                               "storage:filename=iOS-Simulator-MyRNDemoApp.1.3.0-162.zip")  # Verify filename
        options.set_capability("appium:noReset", True)  # Prevent app reset
        options.set_capability("appium:appiumVersion", "2.0.0")
        options.set_capability("browserName", "")
        # Sauce Labs specific options
        options.set_capability("sauce:options", {
            "name": "iOS Simulator App Test",
            #"appiumVersion": "stable",  # This gives a "Invalid Version format used" error if I keep this in test
            "sessionCreationRetry": 2,
            "sessionCreationTimeout": 300000,
            "deviceOrientation" : 'PORTRAIT',
            "extendedDebugging": True  # Enable detailed logging
        })

        # Initialize the Appium driver
        driver = webdriver.Remote(
            command_executor=SAUCE_URL,
            options=options
        )

        # Wait for the app to load
        time.sleep(5)

        # Example test action: Find an element by iOS class chain and interact
        login_button = driver.find_element(AppiumBy.IOS_CLASS_CHAIN,
                                           '**/XCUIElementTypeStaticText[`name == "Product Name"`][1]')
        #Can not find any element as I am not able to get developer tools option in VDC
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
    test_ios_simulator_app()