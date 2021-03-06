import os
import pickle
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, SessionNotCreatedException
from webdriver_auto_update import check_driver

def genshin_daily_login():

    # Setup chrome driver parameters
    PATH_TO_DRIVER = './chromedriver.exe'
    PATH_TO_COOKIES = './cookies.pkl'
    options = Options()
    options.add_argument('--log-level=3')

    # Show chrome if user need to manually log it
    if os.path.isfile(PATH_TO_COOKIES):
        options.headless = True

    service = Service(PATH_TO_DRIVER)

    

    try:
        driver = webdriver.Chrome(service=service, options=options)
    except:
        check_driver('./')
        driver = webdriver.Chrome(service=service, options=options)


    # preload page to evade cookies domain error
    url = 'https://webstatic-sea.mihoyo.com/ys/event/signin-sea/index.html?act_id=e202102251931481&lang=en-us'
    driver.get(url)

    # check if cookies exists
    # if not then let user log in and save cookies
    if not os.path.isfile(PATH_TO_COOKIES):
        input('Log in and then press enter')
        pickle.dump(driver.get_cookies() , open(PATH_TO_COOKIES, 'wb'))

    # load cookies and add them to driver
    cookies = pickle.load(open(PATH_TO_COOKIES, 'rb'))
    for cookie in cookies:
        driver.add_cookie(cookie)

    # reload page with cookies
    driver.get(url)

    # wait for page to be fully loaded
    time.sleep(3)

    # try to get active element and click on it to collect rewards
    # if none active elements found then rewards already gathered
    try:
        reward = driver.find_element(By.CSS_SELECTOR, "div[class*='---active---']")
        reward.click()
        print('Claimed reward')
    except NoSuchElementException:
        print('No reward to claim')

    # save cookies
    pickle.dump(driver.get_cookies() , open(PATH_TO_COOKIES, 'wb'))

    time.sleep(1)

    driver.close()

if __name__ == '__main__':
    genshin_daily_login()