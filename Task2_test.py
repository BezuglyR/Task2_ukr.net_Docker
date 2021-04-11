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

from selenium import webdriver
from time import sleep
import unittest
import random
import string

login = 'romiktest'
password = 'ababagalamaga87'


class Task2Case(unittest.TestCase):
    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1420,1080')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        #self.driver = webdriver.Chrome()
     
    def tearDown(self):
        self.driver.close()

    def test_mail(self):
        driver = self.driver
        driver.implicitly_wait(15)
        # Step 1 --- Login mail
        driver.get('https://accounts.ukr.net/')
        # self.assertIn('Mail @ ukr.net', driver.title)  # Check if page opened
        driver.find_element_by_xpath('//body//button[3]/span[2]').click()  # Switch to English language
        driver.find_element_by_xpath('//form/div//input').send_keys(login)  # Input login
        driver.find_element_by_xpath('//form/div[2]//input').send_keys(password)  # Input password
        driver.find_element_by_xpath('//form/div[3]//input').click()  # Click to check "Public computer"
        driver.find_element_by_xpath('//form/button').click()  # Click next button
        sleep(3)
        # self.assertIn(login + '@ukr.net', driver.title) # Check if log in

        # Step 2 --- Sending mails self
        inbox = len(driver.find_elements_by_xpath('//div[@class="screen__content"]//tbody/tr/td[4]/a'))  # Inbox quantity
        driver.find_element_by_xpath('//div[@id="content"]/aside/button').click()
        for a in range(3):  # Inserting data by loop 3 mails
            # Creating random values
            random1 = ''.join(random.choice(string.letters.lower() + string.digits * 3) for i in range(10))
            random2 = ''.join(random.choice(string.letters.lower() + string.digits * 3) for i in range(10))
            self.assertNotEquals(random1, random2)  # Check if random not equals

            # Input "To", "Subject", "Massage text" and click send in a 3 mails loop
            driver.find_element_by_xpath('//section[@class="sendmsg__form"]/div/div[4]/input[2]') \
                .send_keys(login + '@ukr.net')
            driver.find_element_by_xpath('//section[@class="sendmsg__form"]/div[4]/div[2]/input').send_keys(random1)
            driver.find_element_by_xpath('//*[@class="mce-edit-area mce-container mce-panel mce-stack-layout-item'
                                         ' mce-last"]/iframe').send_keys(random2)
            driver.find_element_by_xpath('//div[@class="controls"]/button').click()

            # In loop click new massage button until last send, after last we click button to return on main mail page
            while (True):
                try:
                    if ((3 - (a + 1)) != 0):
                        driver.find_element_by_xpath('//div[@class="sendmsg__ads-ready"]/button').click()
                        break
                    else:
                        driver.find_element_by_xpath(
                            '//div[@class="sendmsg__ads-ready"]/button[@class="action"]').click()
                        break
                except Exception as e:
                    continue

        # Step 3 --- If all sent mails received
        # In step 2, first of all we check inbox mails quantity before send. On this step we check difference after send.
        new_inbox = len(driver.find_elements_by_xpath('//div[@class="screen__content"]//tbody/tr/td[4]/a'))
        self.assertEqual(new_inbox - 3, inbox)  # new check inbox minus mails to send must be equal to first check inbox

        # Step 4 --- Collect mails data from main page
        dic = {}  # Create new blank dictionary
        mails = driver.find_elements_by_xpath(
            '//div[@class="screen__content"]//tbody/tr/td[4]/a')  # mails subject, text
        for i in mails:  # Add data to dictionary by looping over mails
            t = (i.text).split("  ")  # Split string into 2 separated data
            dic[t[0]] = t[1]  # Adding separated key and value to dictionary
            if (len(dic) == 3):  # If dictionary length become 3 then break loop
                break

        # Step 5 --- Send last mail with collected data from sent before
        driver.find_element_by_xpath('//aside/button').click()  # New mail button
        driver.find_element_by_xpath('//section[@class="sendmsg__form"]/div/div[4]/input[2]') \
            .send_keys(login + '@ukr.net')  # Input To
        driver.find_element_by_xpath('//section[@class="sendmsg__form"]/div[4]/div[2]/input').send_keys('Last Mail')
        for k, v in dic.items():  # Loop over dictionary
            digits = ''.join([n for n in v if n.isdigit()])  # Take digits from string
            letters = ''.join([i for i in v if i.islower()])  # Take letters from string
            text = 'Received mail on theme {} with message: {}. It contains {} letters and {} numbers.'.format(k, v,
                                                                                                               len(
                                                                                                                   letters),
                                                                                                               len(
                                                                                                                   digits))
            driver.find_element_by_xpath('//*[@class="mce-edit-area mce-container mce-panel mce-stack-layout-item'
                                         ' mce-last"]/iframe').send_keys(text + '\n')  # Input text in massage box
        driver.find_element_by_xpath('//div[@class="controls"]/button').click()  # Send mail
        driver.find_element_by_xpath('//div[@class="sendmsg__ads-ready"]/button[@class="action"]').click()
        # Step 6 --- Delete all mails except last one
        driver.find_element_by_xpath('//div[@id="msglist"]//div/label').click()  # Click on check all email
        driver.find_element_by_xpath('//div[@id="msglist"]/div[2]//tbody/tr/td').click()  # Click to uncheck last mail
        driver.find_element_by_xpath('//div[@id="msglist"]/div/div/div[2]/a[2]').click()  # Click delete
        sleep(1)


if __name__ == '__main__':
    unittest.main()
