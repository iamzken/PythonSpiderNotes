# -*- encoding = utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import csv
import os
import time
import re

driver = webdriver.Chrome()


def putcookies(account, password):
    try:
        driver.get('https://www.zhihu.com/#signin')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                        "body > div.index-main > div > div.desk-front.sign-flow.clearfix.sign-flow-simple > div.index-tab-navs > div > a.active")))
        botton = driver.find_element_by_css_selector(
            'body > div.index-main > div > div.desk-front.sign-flow.clearfix.sign-flow-simple > div.view.view-signin > div.qrcode-signin-container > div.qrcode-signin-step1 > div.qrcode-signin-cut-button > span')
        botton.click()
        form = driver.find_element_by_css_selector(
            'body > div.index-main > div > div.desk-front.sign-flow.clearfix.sign-flow-simple > div.view.view-signin > form > div.group-inputs > div.account.input-wrapper > input[type="text"]')
        pas = driver.find_element_by_css_selector(
            'body > div.index-main > div > div.desk-front.sign-flow.clearfix.sign-flow-simple > div.view.view-signin > form > div.group-inputs > div.verification.input-wrapper > input[type="password"]')
        sub = driver.find_element_by_css_selector(
            'body > div.index-main > div > div.desk-front.sign-flow.clearfix.sign-flow-simple > div.view.view-signin > form > div.button-wrapper.command > button')
        form.send_keys(account)
        pas.send_keys(password)
        sub.click()
        try:
            print('please input vcode')
            driver.implicitly_wait(10)
            driver.find_element_by_css_selector(
                '#root > div > div:nth-child(2) > header > div > div.SearchBar > button')
        except NoSuchElementException:
            sub.click()
    except:
        putcookies(account, password)



def change_page(num):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '#root > div > div:nth-child(2) > header > div > div.SearchBar > button')))
    for i in range(num):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(3)



def findinf(html):
    soup = BeautifulSoup(html, 'lxml')
    r = re.compile('(\d+)')
    links = soup.find_all('div', class_='Card TopstoryItem')
    for link in links:
        try:
            maininf = link.find(class_='Feed-meta-item').get_text()[-3:]
            writer = link.find(class_='AuthorInfo-head').get_text()
        except:
            continue
        try:
            intd = link.find('div', class_='RichText AuthorInfo-badgeText').string
        except:
            intd = ''
        title = link.find('h2', class_='ContentItem-title').get_text()
        href = 'https://www.zhihu.com' + link.find('h2', class_='ContentItem-title').a['href']
        try:
            support = link.find(class_='Button VoteButton VoteButton--up').get_text()
        except:
            support = link.find(class_='Button LikeButton ContentItem-action').get_text()
        try:
            talking = r.match(
                link.find('button', class_='Button ContentItem-action Button--plain').get_text()[:-3]).group()
        except:
            talking = ''
        content = link.find('span', class_='RichText CopyrightRichText-richText').get_text()
        yield {
            'maininf': maininf,
            'writer': writer,
            'intd': intd,
            'title': title,
            'support': support,
            'talking': talking,
            'content': content,
            'href': href,
        }


def make(path):
    if not os.path.exists(path):
        os.makedirs(path)


def save_to_csv(inf, path):
    with open(path + 'zhihu.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(['title', 'author', 'topic', 'intro', 'agree', 'talks', 'links', 'digest'])
        try:
            for i in inf:
                writer.writerow(
                    [i['title'], i['writer'], i['maininf'], i['intd'], i['support'], i['talking'], i['href'],
                     i['content']])
        except:
            pass



def main(account, password, num):
    path = 'D:/data/zhihu/'
    putcookies(account, password)
    change_page(num)
    inf = findinf(driver.page_source)
    make(path)
    print('---' * 43)
    print('{:^60}'.format('zhihu'))
    print("***" * 43)
    for i in findinf(driver.page_source):
        print('title:{:<10s}'.format(i['title']))
        print('author:{:>3s}'.format(i['writer']))
        print("topic:{:>3s}".format(i['maininf']))
        print('intro:')
        print('{:<5s}'.format(i['intd']))
        print('agree:{:<2s}'.format(i['support']))
        print("talks:{:3s}".format(i['talking']))
        print("links:" + i['href'])
        print("digest:")
        print('{:<5s}'.format(i['content']))
        print('---' * 43)
    save_to_csv(inf, path)



if __name__ == '__main__':
    num = int(input('pages:'))
    account = input("email:")
    password = input("password:")
    time_start = time.time()
    main(account, password, num)
    print("^^^" * 43)
    print("elapse{}s".format(time.time() - time_start))
    driver.quit()
