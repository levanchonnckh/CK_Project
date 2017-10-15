from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import colorama

# /Users/lechon/Desktop/geckodriver
def checkAlert(host,geck):
    print colorama.Fore.GREEN + "[?] -> Firefox...Running" +colorama.Fore.RESET
    try:
        browser = webdriver.Firefox (executable_path=geck)
    except TimeoutException,e:
        print colorama.Fore.RED +"[!] -> "+ e.message+ colorama.Fore.RESET
    print colorama.Fore.GREEN + "[!] -> Firefox...Success"+colorama.Fore.RESET


    kt = raw_input ("[!] -> Login (y/n): ")
    if kt == 'y':
        browser.get (host)
        # pickle.dump (browser.get_cookies (), open ("QuoraCookies.pkl", "wb"))
        username = browser.find_element_by_id ("login")
        password = browser.find_element_by_id ("password")

        username.send_keys ("bee")
        password.send_keys ("bug")

        browser.find_element_by_name ("form").click ()

    browser.get (host)
    # for cookie in pickle.load(open("QuoraCookies.pkl", "rb")):
    #     browser.add_cookie(cookie)


    try:
        WebDriverWait (browser, 3).until (EC.alert_is_present (),
                                          'Timed out waiting for PA creation ' +
                                          'confirmation popup to appear.')

        alert = browser.switch_to.alert.accept ()
        # alert.accept()
        print colorama.Fore.RED + "[!] -> Alert accepted" +colorama.Fore.RESET
        return True
    except TimeoutException:
        print colorama.Fore.GREEN +"[!] -> No alert" +colorama.Fore.RESET
        return False
