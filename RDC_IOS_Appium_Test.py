#Test Passed on Sauce Labs - Application working properly
import os
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.ios import XCUITestOptions
import time

# Sauce Labs credentials from environment variables
SAUCE_USERNAME = os.environ.get('SAUCE_USERNAME')
SAUCE_ACCESS_KEY = os.environ.get('SAUCE_ACCESS_KEY')
SAUCE_URL = f"https://{SAUCE_USERNAME}:{SAUCE_ACCESS_KEY}@ondemand.us-west-1.saucelabs.com:443/wd/hub"


def test_ios_app():
    driver = None
    try:
        # Initialize AppiumOptions for iOS
        options = XCUITestOptions()
        options.set_capability("platformName", "iOS")
        options.set_capability("appium:platformVersion", "16.7")  # Adjust to match available device version
        options.set_capability("appium:deviceName", "iPhone.*")  # Dynamic device allocation
        options.set_capability("appium:automationName", "XCUITest")
        options.set_capability("appium:app", "storage:filename=SauceLabs-Demo-App.ipa")  # Replace with your app's filename
        options.set_capability("appium:language", "en")
        options.set_capability("appium:locale", "en_US")
        #options.set_capability("appium:appiumVersion", "2.0.0")
        options.set_capability("appium:orientation", "PORTRAIT")
        options.set_capability("autoDismissAlerts",True)
        options.set_capability("newCommandTimeout",360)
        options.set_capability("browserName", "Safari")
        # Sauce Labs specific options
        options.set_capability("sauce:options", {
            "name": "iOS App Test",
            "appiumVersion": "latest",
            "deviceOrientation": "PORTRAIT",
            "sessionCreationRetry": 2,
            "sessionCreationTimeout": 300000,
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
        #time.sleep(5)

        # Example test action: Find an element by accessibility ID and interact
        # Replace 'login_button' with an actual accessibility ID from your app
        login_button = driver.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeStaticText[`name == "Product Name"`][1]')
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
    test_ios_app()