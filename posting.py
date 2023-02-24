import sys

import eel as eel
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import undetected_chromedriver.patcher as chrome_patcher
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import datetime, timezone
from selenium import webdriver
from dateutil import parser
from time import sleep
import threading
import platform
import requests
import random
import json
import uuid
import os
eel.init('web')

api_name = 'writerslab'


def get_provided_licence_details(session_, licence):
    global api_name
    details = session_.get(f'http://pythrack.com/licence/{licence}').json()
    try:
        if details['detail']:
            licence_det = session_.post(f'http://pythrack.com/licence/',
                                        data={'licence': f'{licence}'}).json()
            id_ = licence_det['id']
            session_.post(f'http://pythrack.com/licence/{api_name}/',
                          data={'licence': id_, 'active': True}).json()
            details = session_.get(f'http://pythrack.com/licence/{licence}').json()

    except Exception as e:
        try:
            if details[api_name]['active']:
                pass

        except Exception as e:
            id_ = details['id']
            session_.post(f'http://pythrack.com/licence/{api_name}/',
                          data={'licence': id_, 'active': True})
            details = session_.get(f'http://pythrack.com/licence/{licence}').json()
    active = details[api_name]['active']
    td = parser.parse(details[api_name]['expiry']) - datetime.now(timezone.utc)
    if td.days < 0:
        time_remaining = '0 Days, 0 Hours, 0 Minutes'
    else:
        time_remaining = '{} Days, {} Hours, {} Minutes'.format(td.days, td.seconds // 3600,
                                                                (td.seconds // 60) % 60)
    return active, licence, time_remaining


def data_path(account_name):
    try:
        cwd = os.getcwd()
        path = os.path.join(cwd, account_name)
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    except Exception as e:
        pass


class twitter:
    def __init__(self, data=None):
        """
                :param data:
                {
                    'email': None,
                    'password': None,
                    'username': None,
                    'hashtag':None,
                    'message': None
                    'posting_time': None,
                }
                """
        self.data = data
        self.tagging = "mike"
        self.url = "https://twitter.com/home"
        self.session = requests.Session()
        self.blacklist_titles = []
        self.running = True
        self.minimum_characters = 250
        self.chucked_list = []
        self.blacklisted_treads = ["Tweets"]
        self.tag_list = []
        self.messages_list = []

    def get_computer_licence(self):
        my_system = platform.uname()
        address: str = f"{my_system.node}pythrackbots{my_system.machine}{my_system.processor}".replace(" ", "")
        licence: str = str(uuid.uuid3(uuid.NAMESPACE_DNS, "%s" % address)).replace('-', '')
        return licence[:7] + "_" + self.data['email']

    def messages(self):
        messages = open('data/messages.txt', 'r')
        all_sms = messages.readlines()
        for message_raw in all_sms:
            message = message_raw.split("*")[0]
            try:
                keyword_processed = message.strip()
            except:
                keyword_processed = message

            self.messages_list.append(keyword_processed)

    def hashtag(self):
        messages = open('data/hashtags.txt', 'r')
        all_tags = messages.readlines()
        for message_raw in all_tags:
            tag = message_raw.split(",")[0]
            try:
                hh = tag.strip("#")
                post_tag = "#" + hh + " "
                self.tag_list.append(post_tag)
            except:
                post_tag = "#" + tag + " "
                self.tag_list.append(post_tag)

    def sign_in(self):
        try:
            self.driver.get("https://twitter.com/login")
            email_provision = WebDriverWait(self.driver, 2, poll_frequency=0.2).until(
                EC.visibility_of_element_located((By.XPATH, '//input[@autocapitalize="sentences"]')))
            email_provision.send_keys(self.data['email'])
            sleep(2)
            log_in_button = WebDriverWait(self.driver, 2, poll_frequency=0.2).until(
                EC.visibility_of_element_located((By.XPATH, '//span[contains(text(), "Next")]')))
            log_in_button.click()
            sleep(3)
        except:
            pass
        try:
            username_provision = WebDriverWait(self.driver, 2, poll_frequency=0.2).until(
                EC.visibility_of_element_located((By.XPATH, '//input[@inputmode="text"]')))
            username_provision.send_keys(self.data['username'])
            sleep(1)
            log_in_button = WebDriverWait(self.driver, 2, poll_frequency=0.2).until(
                EC.visibility_of_element_located((By.XPATH, '//span[contains(text(), "Next")]')))
            log_in_button.click()
        except:
            pass
        try:
            password_provision = WebDriverWait(self.driver, 2, poll_frequency=0.2).until(
                EC.visibility_of_element_located((By.XPATH, '//input[@name="password"]')))
            password_provision.send_keys(self.data['password'])
            log_in_button = WebDriverWait(self.driver, 2, poll_frequency=0.2).until(
                EC.visibility_of_element_located((By.XPATH, '//span[contains(text(), "Log in")]')))
            log_in_button.click()
            sleep(3)
        except:
            print("Incorrect email or password !!")
            sleep(2)
            self.driver.quit()
            sys.exit()

    def posting(self):
        while self.running:
            self.driver.get("https://twitter.com/home")
            sleep(2)
            # try:
            #     treading_raw = self.driver.find_elements(By.XPATH, '//div[@data-testid="cellInnerDiv"]//div[2]')
            #     tread_list = []
            #     for trd in treading_raw[1:4]:
            #         trd = trd.text.replace("#", "")
            #         if trd not in self.blacklisted_treads:
            #             tread_list.append(trd)
            # except:
            #     pass
            # self.driver.back()
            try:
                all_titles = self.messages_list
                for message in all_titles:
                    while self.running:
                        writing_section = WebDriverWait(self.driver, 14, poll_frequency=0.2).until(
                            EC.visibility_of_element_located((By.XPATH, '//div[@data-contents="true"]')))
                        if len(message) < 190:
                            for letter in message:
                                writing_section.send_keys(u'\u2666 ' + letter)
                        writing_section.send_keys(Keys.SHIFT, Keys.ENTER)
                        writing_section.send_keys(Keys.SHIFT, Keys.ENTER)
                        writing_section.send_keys(Keys.SHIFT, Keys.ENTER)
                        nt = 7
                        random_tag = ''
                        blacklist_tag = []
                        for tag in range(nt):
                            random_tag = random.choice(self.tag_list)
                            if random_tag not in blacklist_tag:
                                writing_section.send_keys(random_tag)
                                blacklist_tag.append(random_tag)
                        try:
                            image = self.driver.find_element(By.XPATH, '//input[@data-testid="fileInput"]')
                            sleep(2)
                            path = data_path("PosterData")
                            files = os.listdir(path)
                            random_pic_name = random.choice(files)
                            pic_path = path + "\\" + random_pic_name
                            image.send_keys(pic_path)
                            sleep(1)
                        except:
                            pass
                        tweet_button = self.driver.find_element(By.XPATH, '//a[@aria-label="Add Tweet"]/following-sibling::div')
                        tweet_button.click()
                        sleep(2)
                        sleeping_time = self.data['posting_time'] * 60
                        self.driver.get(self.url)
                        sleep(sleeping_time)
                sleep(5)
            except Exception as e:
                sleep(60)
                self.posting()

    def run(self):
        self.poster_data_path = data_path("PosterData")
        self.hashtag()
        self.messages()
        chrome_options = webdriver.ChromeOptions()
        threading.Thread(target=self.check_licence).start()
        patcher = chrome_patcher.Patcher()
        patcher.auto()
        self.driver = webdriver.Chrome(executable_path=patcher.executable_path, options=chrome_options)
        self.driver.maximize_window()
        active, licence_details, time_remaining = get_provided_licence_details(requests.session(),self.get_computer_licence())
        print(licence_details)
        if not active:
            self.terminate()

        else:
            threading.Thread(target=self.check_licence).start()
            self.sign_in()
            self.posting()

    def terminate(self):
        print("Bot running time expired! Kindly contact +254792186745")
        sleep(2)
        print("Bot terminating")
        self.running = False
        print("Bot succesfully terminated")
        self.driver.quit()
        sys.exit()

    def check_licence(self):
        while self.running:
            sleep(80)
            active, licence_details, time_remaining = get_provided_licence_details(requests.session(), self.get_computer_licence())
            if not active:
                self.terminate()


@eel.expose
def write_output():
    sys.stdout.write = eel.report_output


@eel.expose
def tweet_details(user_data):
    twitter_bot = twitter(data=user_data)
    twitter_bot.run()


eel.start('hello.html', size=(450, 600))
