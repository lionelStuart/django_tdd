from selenium import webdriver

HOST = 'http://localhost:8000'


browser = webdriver.Firefox()
browser.get(HOST)

assert 'Django' in browser.title
