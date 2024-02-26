import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import wget
import base64
from io import BytesIO
from PIL import Image
import os


def decodeBase64ToImg(base64String, n, path):
    base64String = base64String.replace("data:image/jpeg;base64,", "")
    binData = base64.b64decode(base64String)
    imageData = BytesIO(binData)
    image = Image.open(imageData)
    #image.show()
    image.convert("RGB")
    image.save(path + '/image' + str(n - 20) + '.png')
    time.sleep(1)
    
    return image



#r = requests.get('http://yahoo.com')
#soup = BeautifulSoup(r.content, 'html5lib')


#prepping

cd = os.getcwd()
ninja = 'ninja'
path = os.path.join(cd, ninja)
if os.path.exists(path):
    print("Ninja is here and always has been.")
else:
    os.makedirs(path)
    print("Ninja has dropped from the battle bus.")



browser = webdriver.Firefox()
browser.get('https://google.com/')
#assert 'Google' in browser.title

elem = browser.find_element(By.NAME, 'q')
elem.send_keys('ninja from fortnite' + Keys.RETURN)

time.sleep(3)

elem = browser.find_element(By.LINK_TEXT, "Images")
elem.click()

time.sleep(3)

windowHandle = browser.current_window_handle

for x in range(80):
    y = (x * 2) + 20
    s = '(//img)[' + str(x + 8) + ']'
    elem = browser.find_element(By.XPATH, s)
    elemSrc = elem.get_attribute('src')
    elemAlt = elem.get_attribute('alt')
    if(elemAlt == ''):
        continue
    browser.switch_to.new_window('tab')
    browser.get(elemSrc)
    time.sleep(2)
    #print(elemSrc)
    fileName = decodeBase64ToImg(elemSrc, x, path)
    browser.close()
    browser.switch_to.window(windowHandle)

#print(elemSrc)
#soup = BeautifulSoup(browser.page_source, 'html5lib')
#s = soup.findAll('div', class_='FMKtTb UqcIvb')
#print(s)

browser.quit()







"""r = requests.get('https://mcloud.bz/e/8z39qv?t=4xjQAf0vBFcOzA%3D%3D&amp;sub.info=https%3A%2F%2Ffmoviesz.to%2Fajax%2Fepisode%2Fsubtitles%2F3127&amp;autostart=true')


print(r)

soup = BeautifulSoup(r.content, 'html5lib')

print(soup.prettify())

#s = soup.find('iframe')
videoTags = soup.findAll('iframe')
print("Total", len(videoTags),"videos found")
print(videoTags)"""