import time
from exceptions import Exception

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


browser = webdriver.Chrome()


url = "https://d3svb6mundity5.cloudfront.net/dashboard/index.html"
browser.get(url)

#element = browser.find_element_by_xpath("//path[@class='opposition marker leaflet-clickable']").click()

#element = browser.find_element_by_css_selector("opposition marker leaflet-clickable").click()


'''
<div class="load_more">
<a class="button button_grey" href="#">Load more</a> 
</div>
'''
#browser.find_element_by_css_selector("div.load_more>a").click()

time.sleep(30)

#elements = browser.find_elements_by_css_selector("g>path.government.marker.leaflet-clickable")

aTagsInLi = browser.find_elements_by_css_selector('div.leaflet-overlay-pane svg g path')
for a in aTagsInLi:
    #print a.get_attribute('class')
    #browser.execute_script("arguments[0].setAttribute('class','__web-inspector-hide-shortcut__')", a)
    #browser.execute_script("arguments[0].setAttribute('style','__web-inspector-hide-shortcut__')", a)
    browser.execute_script("arguments[0].setAttribute('style', 'visibility:hidden')", a)

cont = 0
con2 = 0
for a in aTagsInLi:
    #print a.get_attribute('class')
    #browser.execute_script("arguments[0].setAttribute('class','__web-inspector-hide-shortcut__')", a)
    #browser.execute_script("arguments[0].setAttribute('style','__web-inspector-hide-shortcut__')", a)

    try:
        browser.execute_script("arguments[0].setAttribute('style', 'visibility:visible')", a)
        a.click()
        contenido = browser.find_element_by_css_selector('div.event-name')
        print "{0}: {1}".format(cont, contenido.text)
        cont = cont + 1
        time.sleep(1)
        browser.execute_script("arguments[0].setAttribute('style', 'visibility:hidden')", a)
    except Exception:
        con2 = con2 + 1
        browser.execute_script("arguments[0].setAttribute('style', 'visibility:hidden')", a)
        continue
