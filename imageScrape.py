import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import base64
from io import BytesIO
from PIL import Image
import os

def base64ToData(base64String, type):
    base64String = base64String.replace("data:image/" + type + ";base64,", "")
    binData = base64.b64decode(base64String)
    return BytesIO(binData)

def decodeBase64ToImg(base64String, n, path):
    if "data:image/jpeg;base64," in base64String:
        imageData = base64ToData(base64String, "jpeg")
    
    elif "data:image/png;base64," in base64String:
        imageData = base64ToData(base64String, "png")

    elif "data:image/gif;base64," in base64String:
        imageData = base64ToData(base64String, "gif")
   
    elif "https" in base64String:
        r = requests.get(base64String)
        imageData = BytesIO(r.content)
    else:
        print(base64String)
        print("Unkown image format")

    try:
        image = Image.open(imageData)
        image.convert("RGB")
        image.save(path + '/image' + str(n - 20) + '.png')
    except Exception as e:
        print(f"Error processing image {n}: {e}")

    return image

def openingImageTab(browser):
    elem = browser.find_element(By.LINK_TEXT, "Images")
    elem.click()
    time.sleep(1)
    elem = browser.find_element(By.XPATH, '/html/body/div[2]/c-wiz/div[1]/div/div[1]/div[2]/div[2]/div')         #selects tools
    elem.click()
    elem = browser.find_element(By.XPATH, "/html/body/div[2]/c-wiz/div[2]/div[2]/c-wiz[1]/div/div/div[1]/div/div[1]/div/div[1]")            #selects size
    elem.click()
    elem = browser.find_element(By.XPATH, "/html/body/div[2]/c-wiz/div[2]/div[2]/c-wiz[1]/div/div/div[3]/div/a[2]")         #selects large
    elem.click()


#prepping

print("This is a program that will take a Google search as input and a folder name as input. It will then preview images from the Google Search and then download them.")

folder = input("\nWhat would you like the folder to be called?: ")

cd = os.getcwd()
path = os.path.join(cd, folder)
if os.path.exists(path):
    print(folder + " is here and always has been.")
else:
    os.makedirs(path)
    print(folder +" has dropped from the battle bus.")


#opening browser

search = input("\nWhat would you like the search to be?: ")

browser = webdriver.Firefox()
browser.get('https://google.com/')
assert 'Google' in browser.title

elem = browser.find_element(By.NAME, 'q')
elem.send_keys(search + Keys.RETURN)


time.sleep(1)

openingImageTab(browser)

time.sleep(1)

windowHandle = browser.current_window_handle

#Display/Download loop

for x in range(80):
    y = x + 50            #this is to skip the first 50 images because most of them are either irrelevant or to small
    s = '(//img)[' + str(y) + ']'
    elem = browser.find_element(By.XPATH, s)
    elemSrc = elem.get_attribute('src')
    if elemSrc == None:
        continue
    elemAlt = elem.get_attribute('data-sz')
    if(elemAlt == "16"):
        continue            #This line should skip icons
    browser.switch_to.new_window('tab')
    browser.get(elemSrc)
    time.sleep(1)
    decodeBase64ToImg(elemSrc, x, path)
    browser.close()
    browser.switch_to.window(windowHandle)


browser.quit()

