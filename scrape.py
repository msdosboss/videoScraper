import requests
from bs4 import BeautifulSoup

r = requests.get('https://www.youtube.com/watch?v=wDchsz8nmbo')


print(r)

soup = BeautifulSoup(r.content, 'html5lib')

print(soup.prettify())

#s = soup.find('iframe')
videoTags = soup.findAll('iframe')
print("Total", len(videoTags),"videos found")
print(videoTags)