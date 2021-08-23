from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time as tm
import pandas as pd

from fb_crawler.setting import CHROMEDRIVER_EXE_DIR
from fb_crawler.setting import FB_ACCOUNT
from fb_crawler.setting import FB_PASSWORD
from db_wrapper import DBWrapper


# 設定 webdriver 的參數，這個 prefs 是關掉Facebook通知
PREFS = {"profile.default_content_setting_values.notifications": 2}


class FaceBookCrawler:
    def __init__(self, url, name, util):
        self.url = url
        self.name = name
        self.util = util
        self.chrome_options = webdriver.ChromeOptions().add_experimental_option("prefs", PREFS)
        self.account = FB_ACCOUNT
        self.password = FB_PASSWORD
        self.driver = webdriver.Chrome(CHROMEDRIVER_EXE_DIR, chrome_options=self.chrome_options)
        self.post_div = ""
        self.p_links = []  # 開三個 list 暫存解析的資料
        self.p_time = []
        self.p_content = []

    def run(self):
        self.go_to_web_site()
        self.maximize_fb_window()
        self.close_login_wins_or_login()
        self.get_soup()
        self.get_fb_posts()
        self.save_to_xlsx()
        self.save_to_db()
        self.driver.quit()

    def go_to_web_site(self):
        self.driver.get(self.url)  # 以瀏覽器打開網址並最大化視窗

    def maximize_fb_window(self):
        self.driver.maximize_window()  # 視窗最大化

    def close_login_wins_or_login(self):
        if self.url.split("/")[-2] == "posts":
            self.login_fb_a()
            # # 關閉登入視窗
            # self.driver.execute_script("window.scrollTo(0,0.5 * document.body.scrollHeight);")
            # tm.sleep(3)  # self.driver.implicitly_wait(10)
            # # x = self.driver.find_element_by_class_name("sx_a5c5d2")
            # x.click()
        else:
            self.login_fb_b()  # 進行登入

    def login_fb_a(self):
        login = self.driver.find_element_by_xpath('// *[ @ id = "mobile_login_bar"] / div[2] / div / a[1]')
        self.do_login(login)

    def login_fb_b(self):
        login = self.driver.find_element_by_xpath('//*[@id="mobile_login_bar"]/div[2]/a[2]')
        self.do_login(login)

    def do_login(self, login):
        login.click()
        tm.sleep(3)  # self.driver.implicitly_wait(5)
        login_acc = self.driver.find_element_by_id("m_login_email")
        login_acc.send_keys(self.account)
        login_pw = self.driver.find_element_by_id("m_login_password")
        login_pw.send_keys(self.password)
        login_pw.send_keys(Keys.RETURN)

    def get_soup(self):
        counter = 0
        while counter < 2:
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            tm.sleep(3)  # self.driver.implicitly_wait(5)
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            tm.sleep(3)  # self.driver.implicitly_wait(5)
            counter += 1
        soup = BeautifulSoup(self.driver.page_source, "lxml")
        self.post_div = soup.find_all("article")

    def get_fb_posts(self):
        # 抓到每一則貼文的層級
        for j, i in enumerate(self.post_div):
            # 貼文內容
            try:
                self.p_content.append(''.join([k.text for k in i.find('header').find_next_siblings()]))
                # str.join() 方法用於將序列中的元素以指定的特定符號或文字(str))串接成新的字串
            except:
                self.p_content.append('')
                print('content' + str(j))
            # 貼文時間
            try:
                self.p_time.append(i.find("header").find("abbr").text)
            except AttributeError:
                try:
                    self.p_time.append(i.find("header").find_next_sibling().find('abbr').text)
                except:
                    self.p_time.append('')
                    print('time' + str(j))

            # 貼文連結
            try:
                self.p_links.append(i.find("header").find('h3').find_next_sibling().find('a')['href'])
            except:
                try:
                    self.p_links.append(i.find("header").find('a')['href'])
                except:
                    self.p_links.append('')
                    print('link' + str(j))

    def save_to_xlsx(self):
        # 使用 pandas 寫入 excel 檔案
        df = pd.DataFrame({
            'p_time': self.p_time,
            'p_content': self.p_content,
            'p_links': self.p_links,
        })
        # df.drop_duplicates()
        df.to_excel(self.util.get_output_filepath(self.name), encoding="utf-8")

    def save_to_db(self):
        db = DBWrapper()
        for time, content, link in zip(self.p_time, self.p_content, self.p_links):
            db.insert_post(self.name, time, content, link)
