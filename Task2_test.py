'''Test Case Steps:
 1. Login into mail
 2. Send 15 mails to self mail(from step 1). Subject random 10 length string witch contains letters and numbers.
     Massage test is random 10 length string witch contains letters and numbers.
 3. Check if all 15 mails received(inbox)
 4. Collect subjects and massages text from mail main page into dict, where key=subject value=text
 5. Send collected info from dict to self mail, massage text format : "Received mail on theme {subject}
     with message: {massage text}. It contains {quantity letters in text} letters and {quantity numbers in text}
     numbers". In this format, must input for all 15 mails.
 6. Delete all mails except last one.'''
from selenium.webdriver.common import by
from selenium.webdriver.support import expected_conditions as ec

from selenium import webdriver
from time import sleep
import chromedriver_binary
import unittest
import random
import string

from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import text_to_be_present_in_element
from selenium.webdriver.support.wait import WebDriverWait

login = 'romiktest'
password = 'ababagalamaga87'
dr_wait = 15
mails_to_send = 3

class Task2Case(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--headless')
        options.add_argument('user-agent=User-Agent: Chrome/89.0.4389.114')
        self.driver = webdriver.Chrome(options=options)
     
    def tearDown(self):
        self.driver.close()

    def test_mail(self):
        driver = self.driver
        driver.implicitly_wait(dr_wait)
        # Step 1 --- Login mail
        driver.get('https://accounts.ukr.net/')
        self.assertIn(' @ ukr.net', driver.title)  # Check if page opened
        driver.find_element_by_xpath('//button/span[text()="English"]').click()  # Switch to English language
        driver.find_element_by_xpath('//input[@name="login"]').send_keys(login)  # Input login
        driver.find_element_by_xpath('//input[@name="password"]').send_keys(password)  # Input password
        driver.find_element_by_xpath('//input[@type="checkbox"]').click()  # Click to check "Public computer"
        driver.find_element_by_xpath('//button[@type="submit"]').click()  # Click next button
        wait = WebDriverWait(driver, dr_wait)
        wait.until(ec.title_contains('@ukr.net'))
        self.assertIn(login + '@ukr.net', driver.title) # Check if log in

        # Step 2 --- Sending mails self
        inbox = len(driver.find_elements_by_xpath('//tbody/tr[contains(@class, "msglist")]'))  # Inbox quantity
        driver.find_element_by_xpath('//button[text()="Compose"]').click()
        for a in range(mails_to_send):  # Inserting data by loop 15 mails
            # Creating random values
            random1 = ''.join(random.choice(string.letters.lower() + string.digits * 3) for i in range(10))
            random2 = ''.join(random.choice(string.letters.lower() + string.digits * 3) for i in range(10))
            self.assertNotEquals(random1, random2)  # Check if random not equals

            # Input "To", "Subject", "Massage text" and click send in a 15 mails loop
            driver.find_element_by_xpath('//input[contains(@name, "toFieldInput")]').send_keys(login + '@ukr.net')
            driver.find_element_by_xpath('//input[contains(@name, "subject")]').send_keys(random1)
            driver.find_element_by_xpath('//div[contains(@class, "mce-edit-area")]/iframe').send_keys(random2)
            driver.find_element_by_xpath('//div[contains(@class, "sendmsg")]/button[text()="Send"]').click()

            # In loop click new massage button until last send, after last we click button to return on main mail page
            while (True):
                try:
                    if ((mails_to_send - (a + 1)) != 0):
                        driver.find_element_by_xpath('//button[text()="Compose more"]').click()
                        break
                    else:
                        driver.find_element_by_xpath('//button[text()="return to inbox"]').click()
                        break
                except Exception as e:
                    continue

        # Step 3 --- If all sent mails received
        # In step 2, first of all we check inbox mails quantity before send. On this step we check difference after send.
        wait.until(ec.title_contains('@ukr.net'))
        new_inbox = len(driver.find_elements_by_xpath('//tbody/tr[contains(@class, "msglist")]'))
        self.assertEqual(new_inbox - mails_to_send, inbox)  # new check inbox minus mails to send must be equal to first check inbox

        # Step 4 --- Collect mails data from main page
        dic = {}  # Create new blank dictionary
        mails = driver.find_elements_by_xpath('//td[contains(@class, "row-subject")]')  # mails subject, text
        for i in mails:  # Add data to dictionary by looping over mails
            t = (i.text).split("  ")  # Split string into 2 separated data
            dic[t[0]] = t[1]  # Adding separated key and value to dictionary
            if (len(dic) == mails_to_send):  # If dictionary length become 15 then break loop
                break

        # Step 5 --- Send last mail with collected data from sent before
        driver.find_element_by_xpath('//button[text()="Compose"]').click()  # New mail button
        driver.find_element_by_xpath('//input[contains(@name, "toFieldInput")]').send_keys(login + '@ukr.net')  # Input To
        driver.find_element_by_xpath('//input[contains(@name, "subject")]').send_keys('Last Mail')
        for k, v in dic.items():  # Loop over dictionary
            digits = ''.join([n for n in v if n.isdigit()])  # Take digits from string
            letters = ''.join([i for i in v if i.islower()])  # Take letters from string
            text = 'Received mail on theme {} with message: {}. It contains {} letters and {} numbers.'.format(k, v,
                                                                                                               len(
                                                                                                                   letters),
                                                                                                               len(
                                                                                                                   digits))
            driver.find_element_by_xpath('//div[contains(@class, "mce-edit-area")]/iframe').send_keys(text + '\n')  # Input text in massage box
        driver.find_element_by_xpath('//div[contains(@class, "sendmsg")]/button[text()="Send"]').click()  # Send mail
        driver.find_element_by_xpath('//button[text()="return to inbox"]').click()
        # Step 6 --- Delete all mails except last one
        driver.find_element_by_xpath('//div[contains(@class, "msglist__checkbox")]/label').click()  # Click on check all email
        driver.find_element_by_xpath('//tbody/tr[contains(@class, "msglist")]/td[contains(@class, "row-check")]').click()  # Click to uncheck last mail
        driver.find_element_by_xpath('//div[@class="msglist__controls"]/a[text()="Delete"]').click()  # Click delete
        sleep(1)


if __name__ == '__main__':
    unittest.main()
