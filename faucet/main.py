from selenium import webdriver
from enum import Enum
import time
from datetime import datetime
from decouple import config
import os

os.environ['MOZ_HEADLESS'] = '1'

address = config('ADDRESS')
token = config('TOKEN')

print("address", address)
print("token", token)

driver = ""

def getDriver():
    global driver
    try:
        options = webdriver.ChromeOptions()
        driver = webdriver.Remote(command_executor="http://seleniumgrid:4444",
            desired_capabilities=webdriver.DesiredCapabilities.CHROME, options=options)
        # driver = webdriver.Chrome(options=options, desired_capabilities=webdriver.DesiredCapabilities.CHROME)
    except Exception as e:
        time.sleep(1)
        # print(e)
        getDriver()

getDriver()


def faucet(token, address):
    try:
        # options = webdriver.ChromeOptions()
        # driver = webdriver.Remote(command_executor="http://localhost:4444",
        #     desired_capabilities=webdriver.DesiredCapabilities.CHROME, options=options)
        # #driver = webdriver.Firefox()
        driver.get("https://faucet.matic.network")
        

        if token == "MATIC":
            radioElement = driver.find_element_by_css_selector("input[type='radio'][value='maticToken']")
            radioElement.click()
        elif token == "LINK":
            radioElement = driver.find_element_by_css_selector("input[type='radio'][value='link']")
            radioElement.click()
        else:
            print("unsupported token")
            return

        radioElement = driver.find_element_by_css_selector("input[type='radio'][value='mumbai']")
        radioElement.click()

        input = driver.find_element_by_css_selector("input[type='text'][placeholder='Enter your account address']")
        input.send_keys(address)

        buttons = driver.find_elements_by_css_selector("button")
        for button in buttons:
            if button.get_attribute("innerHTML") == "Submit":
                button.click()
                break
        time.sleep(3)
        buttons = driver.find_elements_by_css_selector("button")
        for button in buttons:
            if button.get_attribute("innerHTML") == "Confirm":
                button.click()
                break
        time.sleep(5)

        texts = driver.find_elements_by_css_selector("p.card-header-title")
        found = False
        for text in texts:
            if text.get_attribute("innerHTML") == "Tx success:":
                found = True
                print("The transaction is success")
                links = driver.find_elements_by_css_selector("a[target='_blank']")
                for link in links:
                    href = link.get_attribute('href')
                    if href[:35] == 'https://mumbai-explorer.matic.today':
                        print("transaction link: https://mumbai.polygonscan.com/tx/" + href[39:])
                        return
                return
        if not found:
            print("The transaction doesn't seem to be success")
            cardHeaders = driver.find_elements_by_css_selector("p.card-header-title")
            for header in cardHeaders:
                if header.get_attribute('innerHTML') == 'Error':
                    parent = header.parent
                    content = parent.find_element_by_css_selector("div.card-content")
                    print("Reason:",content.get_attribute("innerHTML"))
            print("retrying")
            time.sleep(60)
            faucet(token, address)
        driver.close()
        driver.quit()
    except Exception as e:
        print("Error:", e)
        print("retrying")
        time.sleep(60)
        faucet(token, address)

faucet(token, address)

# while True:
#     now = datetime.now()
#     if (now.hour == 7 and now.minute == 0) or (now.hour == 18 and now.minute == 0):
#         faucet(token, address)
#         time.sleep(60)

    