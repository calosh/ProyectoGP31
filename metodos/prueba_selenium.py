import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


browser = webdriver.Chrome()


url = "https://twitter.com/search?l=es&q=femicidio%20since%3A2016-01-01%20until%3A2016-01-02&src=typd&lang=es"
browser.get(url)
time.sleep(1)

body = browser.find_element_by_tag_name('body')
clase = ".tweet.js-stream-tweet.js-actionable-tweet.js-profile-popup-actionable.dismissible-content.original-tweet.js-original-tweet"
#find_element_by_css_selector(".action-btn.cancel.alert-display")
tweets = body.find_element_by_css_selector(clase)

cont = 0
innerHTML = ""
while True:
    body.send_keys(Keys.PAGE_DOWN)
    print "si"
    time.sleep(0.2)
    print cont

    if cont == 1:
        innerHTML = body.get_attribute('innerHTML')
        break
    try:
        print body.find_elements_by_class_name('js-tweet-text-container')[cont].text
    except IndexError:
        innerHTML = body.get_attribute('innerHTML')
        break
    cont = cont +1



print innerHTML
html_doc = BeautifulSoup(innerHTML, 'html.parser')
print html_doc
#browser.close()


