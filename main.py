#coding:UTF-8

#libraries needs to be installed
#selenium, pyyaml, slackclient, bs4, lxml

# get ChromeDriver from here
# https://sites.google.com/a/chromium.org/chromedriver/downloads

from __future__ import absolute_import, division, print_function

import sys
import json
import re

import datetime
import time

import urllib

from selenium import webdriver
from selenium.webdriver.support.events import EventFiringWebDriver
from selenium.webdriver.support.events import AbstractEventListener

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import json
import yaml
from slackclient import SlackClient

#defalut value
SLACK_TOKEN = ''
SLACK_USER_ID = ''
#loading credentials
with open("credentials.yaml","r") as stream:
    try:
        credentials = yaml.load(stream)
        globals().update(credentials)
    except yaml.YAMLError as exc:
        print(exc)

FORMAT = "%Y-%m-%d %H:%M:%S"

DO_SHUSSHA = True
DO_TAISHA = False

def post_ephemeral(channel, message):
    sc = SlackClient(SLACK_TOKEN)
    sc.api_call(
        "chat.postMessage",
        channel=channel,
        text=message,
        user=SLACK_USER_ID
    )

def post_message(channel, message):
    sc = SlackClient(SLACK_TOKEN)
    sc.api_call(
        "chat.postEphemeral",
        channel=channel,
        text=message,
        user=SLACK_USER_ID
    )


def delete_reminder(reminder_id):
    sc = SlackClient(SLACK_TOKEN)
    return sc.api_call(
        "reminders.delete",
        token=SLACK_TOKEN,
        reminder=reminder_id
    )

def post_reminder(text,time):
    sc = SlackClient(SLACK_TOKEN)
    return sc.api_call(
        "reminders.add",
        token=SLACK_TOKEN,
        text=text,
        time=int(time),
        user=SLACK_USER_ID,
        pretty=1
    )

class ScreenshotListener(AbstractEventListener):
    def on_exception(self, exception, driver):
        screenshot_name = "00_exception.png"
        driver.get_screenshot_as_file(screenshot_name)
        print("Screenshot saved as '%s'" % screenshot_name)




################## main starts here ##################################

sc = SlackClient(SLACK_TOKEN)

options = Options()
#options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1042,770')
_driver = webdriver.Chrome(chrome_options=options)
driver = EventFiringWebDriver(_driver, ScreenshotListener())

#_driver = webdriver.PhantomJS()
#driver = EventFiringWebDriver(_driver, ScreenshotListener())

try:
    print( 'drive start' )
    url = "https://www1.j-motto.co.jp/fw/dfw/po80/portal/jsp/J10201.jsp?https://www1.j-motto.co.jp/fw/dfw/gws/cgi-bin/aspioffice/iocjmtgw.cgi?cmd=login"

    driver.get(url)
    driver.implicitly_wait(10)

    memberId_box = driver.find_element_by_id('memberID')
    userId_box = driver.find_element_by_id('userID')
    pass_box = driver.find_element_by_id('password') 
    memberId_box.send_keys(JMOTTO_GROUP)
    userId_box.send_keys(JMOTTO_USERNAME)
    pass_box.send_keys(JMOTTO_PASSWORD)

    driver.save_screenshot('0before login.png')
    print( "saved before login" )

    #login
    driver.find_element_by_name('NAME_DUMMY04').click()

    #elemは特に使わないが、ページが表示されるまで待ちたいため入れている
    elem = driver.find_element_by_css_selector(".portal-cal-body")

    driver.save_screenshot('1after login.png')
    print( "saved after login" )


except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
finally:
    None
    #driver.quit()

