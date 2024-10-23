import requests
from bs4 import BeautifulSoup  
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
from selenium.webdriver.common.action_chains import ActionChains

class scrapper:

    page_limit = 3

    def __init__(self, urls : list) -> None:
        
        options = webdriver.ChromeOptions()
        options.page_load_strategy = 'normal'
        options.add_argument('--disable-blink-features=AutomationControlled')

        self.review_data = pd.DataFrame()
        self.urls = urls
        self.driver = webdriver.Chrome(options=options)

    @classmethod
    def upadate_page_limit(cls, upadated_page_limit : int) -> None:
        cls.page_limit = upadated_page_limit

    def load_more_pages(self, click : str, focus : str = None) -> None:
        
        if focus:     
            hover = self.driver.find_element(By.CLASS_NAME, focus)
            button = self.driver.find_element(By.CLASS_NAME, click)
            ActionChains(self.driver).move_to_element(hover).click(button).perform()
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, focus)))
        
        else:
            button = self.driver.find_element(By.CLASS_NAME, click)
            ActionChains(self.driver).move_to_element(button).click(button).perform()
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, button)))

    def find_spoilers(self) -> zip:
        
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "ipc-btn.ipc-btn--single-padding.ipc-btn--center-align-content.ipc-btn--default-height.ipc-btn--core-base.ipc-btn--theme-base.ipc-btn--on-error.ipc-btn--rounded.ipc-text-button.sc-77f6e511-1.ffVQZx.review-spoiler-button")))

        spoiler_spans = self.driver.find_elements(By.CLASS_NAME,"ipc-icon.ipc-icon--expand-more.ipc-btn__icon.ipc-btn__icon--post")
        
        spoiler_buttons = self.driver.find_elements(By.CLASS_NAME, "ipc-btn.ipc-btn--single-padding.ipc-btn--center-align-content.ipc-btn--default-height.ipc-btn--core-base.ipc-btn--theme-base.ipc-btn--on-error.ipc-btn--rounded.ipc-text-button.sc-77f6e511-1.ffVQZx.review-spoiler-button")

        return zip(spoiler_buttons,spoiler_spans)

    def open_spoilers(self) -> None:

        spoilers = self.find_spoilers()

        for find,click in spoilers:
                ActionChains(self.driver).move_to_element(find).click(click).perform()

    def scrape_old_version(self) -> pd.DataFrame:
        
        contents, ratings, review_titles, reviews = [], [], [], []

        for page in range(self.page_limit):
            try:
                self.load_more_pages("ipl-load-more__button")
            except ElementNotInteractableException:
                continue
            except NoSuchElementException:
                print("Element not found. Page source structure may have changed.")
                    
        movie_title = self.driver.find_element(By.CLASS_NAME, "parent").text
        
        container = self.driver.find_elements(By.CLASS_NAME, "review-container")

        for item in container:
            contents.append(item.get_attribute("outerHTML"))         
    
        for content in contents:
            soup = BeautifulSoup(content, features="html.parser")
            if soup.find("div", class_="ipl-ratings-bar"):
                ratings.append(str(soup.find("div", class_="ipl-ratings-bar")).split("<span>")[1].split("</span")[0])
                review_titles.append(str(soup.find("a", class_="title")).split(">")[1].split("<")[0].split("\n")[0])
                reviews.append(str(soup.find("div", class_="content")).split('<div class="content">')[1].split('</div>')[0].replace('<br/><br/>'," ").split(">")[1])
        
        num_reviews = len(ratings)
        movie_titles = [movie_title]*num_reviews
        
        reviews_df = pd.DataFrame({'movie_title':movie_titles, 'review_title':review_titles, 'review':reviews, 'rating':ratings})
        
        print("Scraped: ", self.url)

        return reviews_df

    def scarpe_new_version(self) -> pd.DataFrame:
        
        contents, ratings, review_titles, reviews = [], [], [], []

        self.open_spoilers()

        for page in range(self.page_limit):
            try:
                self.load_more_pages("ipc-see-more.sc-33e570c-0.cMGrFN.single-page-see-more-button", "ipc-icon.ipc-icon--expand-more.ipc-btn__icon.ipc-btn__icon--post")
                self.open_spoilers()
            except ElementNotInteractableException:
                continue
            except NoSuchElementException:
                print("Element not found. Page source structure may have changed.")
                    
        movie_title = self.driver.find_element(By.CLASS_NAME, "sc-b8cc654b-9.dmvgRY").text
        
        container = self.driver.find_elements(By.CLASS_NAME, "ipc-list-card__content")

        for item in container:
            contents.append(item.get_attribute("outerHTML"))      
    
        for content in contents:
            soup = BeautifulSoup(content, features="html.parser")
            if soup.find("span", class_="ipc-rating-star ipc-rating-star--base ipc-rating-star--otherUserAlt review-rating") and soup.find("div", class_="ipc-html-content-inner-div"):
                ratings.append(str(soup.find("span", class_="ipc-rating-star--rating")).split("</span>")[0].split(">")[1])
                review_titles.append(str(soup.find("span", class_="sc-77f6e511-7 lDIfw")).split("</span>")[0].split(">")[1])
                reviews.append(str(soup.find("div", class_="ipc-html-content-inner-div")).split("</div>")[0].split('''">''')[1].replace("br/","").replace("<>",""))
        
        num_reviews = len(ratings)
        movie_titles = [movie_title]*num_reviews
        
        reviews_df = pd.DataFrame({'movie_title':movie_titles, 'review_title':review_titles, 'review':reviews, 'rating':ratings})
        
        print("Scraped: ", self.url)

        return reviews_df

    def scrape(self, url : str) -> pd.DataFrame:

        self.url = url
        self.driver.get(self.url)
        parsed = False
        
        print("Trying to scrape: ", url)

        try:
            print("Trying to parse through new version.")
            self.driver.find_element(By.CLASS_NAME, "ipc-btn.ipc-btn--single-padding.ipc-btn--center-align-content.ipc-btn--default-height.ipc-btn--core-base.ipc-btn--theme-base.ipc-btn--on-accent2.ipc-btn--rounded.ipc-text-button.ipc-see-more__button")
        except NoSuchElementException:
            print("Element not found.")
        else:
            parsed = True
            return self.scarpe_new_version()

        try:
            print("Trying to parse through old version.")
            self.driver.find_element(By.CLASS_NAME, "ipl-load-more__button")
        except NoSuchElementException:
            print("Element not found.")
        else:
            parsed = True
            return self.scrape_old_version()

        if not parsed:
            print("Either page source structure has changed or incorrect url.")
            return pd.DataFrame()

    def get_reviews(self) -> pd.DataFrame:

        for url in self.urls:
            url_data = self.scrape(url)
            if not url_data.empty:
                self.review_data = pd.concat([self.review_data, url_data],ignore_index=True)
        
        self.driver.quit()
        return self.review_data

if __name__ == "__main__":
    urls = ['https://www.imdb.com/title/tt1745960/reviews/?ref_=tt_ql_urv']
    ws = scrapper(urls)
    data = ws.getReviews()
    if not data.empty:
        print(data)