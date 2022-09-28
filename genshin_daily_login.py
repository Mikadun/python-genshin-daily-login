import os
import pickle
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, InvalidCookieDomainException, \
    SessionNotCreatedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_auto_update import check_driver


def genshin_daily_login(headless=True, force_login=False):
    # Setup chrome driver parameters
    path_to_driver = './chromedriver.exe'
    path_to_cookies = './cookies.pkl'
    options = Options()
    options.add_argument('--log-level=3')

    # Show chrome if user need to manually log it
    options.headless = headless

    if not os.path.isfile(path_to_cookies) or force_login:
        options.headless = False

    service = Service(path_to_driver)

    try:
        driver = webdriver.Chrome(service=service, options=options)
    except SessionNotCreatedException:
        check_driver('./')
        driver = webdriver.Chrome(service=service, options=options)


    # preload page to evade cookies domain error
    url = 'https://webstatic-sea.mihoyo.com/ys/event/signin-sea/index.html?act_id=e202102251931481&lang=en-us'

    driver.get(url)
    
    # check if cookies exists
    # and if is not then let user log in and save cookies
    if not os.path.isfile(path_to_cookies) or force_login:
        input('Log in and then press enter')
        pickle.dump(driver.get_cookies(), open(path_to_cookies, 'wb'))

    # load cookies and add them to driver
    cookies = pickle.load(open(path_to_cookies, 'rb'))
    for cookie in cookies:
        driver.add_cookie(cookie)

    # reload page with cookies
    driver.get(url)

    # wait for page to be fully loaded
    time.sleep(3)

    # try to get active element and click on it to collect rewards
    # if none active elements found then rewards already gathered
    try:
        reward = driver.find_element(By.CSS_SELECTOR, "div[class*='---active']")

        driver.execute_script("arguments[0].click();", reward)

        print('Claimed reward')
    except NoSuchElementException:
        print('No reward to claim')

    # save cookies
    pickle.dump(driver.get_cookies(), open(path_to_cookies, 'wb'))

    time.sleep(1)

    driver.close()


if __name__ == '__main__':
    try:
        genshin_daily_login()
    # this error might happen when cookies get old or site changes
    except InvalidCookieDomainException:
        genshin_daily_login(force_login=True)
