from selenium import webdriver

browser = webdriver.Remote("http://docker.local.com:4444/wd/hub", webdriver.DesiredCapabilities.FIREFOX)

browser.get('http://docker.local.com')

assert 'License Generator' in browser.title, "Browser title was: " + browser.title

browser.quit()