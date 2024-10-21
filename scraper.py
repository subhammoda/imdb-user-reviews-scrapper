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
import old_version_xpaths

class scrapper:

    pages = 2
    old_version_check = old_version_xpaths.old_version
    new_version_check = '/html/body/div[2]/main/div/section/div/section/div/div[1]/section[1]/div[3]/div/span[1]/button'

    def __init__(self, urls : list) -> None:
        
        options = webdriver.ChromeOptions()
        options.page_load_strategy = 'normal'

        self.review_data = pd.DataFrame()
        self.urls = urls
        self.driver = webdriver.Chrome(options=options)

    @classmethod
    def upadate_pages(cls, upadated_pages) -> None:
        cls.pages = upadated_pages

    @classmethod
    def upadate_old_version_check(cls, upadated_old_version) -> None:
        cls.old_version_check = upadated_old_version
    
    @classmethod
    def upadate_new_version_check(cls, upadated_new_version) -> None:
        cls.new_version_check = upadated_new_version

    def scrape(self, url : str) -> pd.DataFrame:

        self.driver.get(url)
        version_check = None
        contents, ratings, review_titles, reviews = [], [], [], []
        
        try:
            self.driver.find_elements(By.XPATH, self.new_version_check)
            if self.driver.find_elements(By.XPATH, self.new_version_check):
                version_check = "new"
                print("version loaded: ", version_check)
        except NoSuchElementException:
            print("Element not found. Trying another version.")

        try:
            self.driver.find_elements(By.XPATH, self.old_version_check)
            if self.driver.find_elements(By.XPATH, self.old_version_check):
                version_check = "old"
                print("version loaded: ", version_check)
        except NoSuchElementException:
            print("Element not found. Page source structure may have changed.")

        if version_check == "old":
            load_more_button = self.driver.find_element(By.CLASS_NAME,'ipl-load-more__button')
    
            for page in range(self.pages-1):
                try:
                    load_more_button.click()
                    WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.CLASS_NAME, "ipl-load-more__button")))
                except ElementNotInteractableException:
                    continue
                except NoSuchElementException:
                    print("Element not found. Page source structure may have changed.")
                        
            movie_title = self.driver.find_element(By.CLASS_NAME, "parent").text
            
            container = self.driver.find_elements(By.CLASS_NAME, "review-container")
            
            self.driver.quit()

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
            
            return reviews_df

        elif version_check == "new":
            pass

        else:
            print("Page source code changed")
        

    def getReviews(self) -> pd.DataFrame:
        for url in self.urls:
            url_data = self.scrape(url)
            self.review_data = pd.concat([self.review_data, url_data],ignore_index=True)

        return self.review_data

if __name__ == "__main__":
    urls = ['https://www.imdb.com/title/tt1745960/reviews/?ref_=tt_ql_urv']
    ws = scrapper(urls)
    data = ws.getReviews()
    print(data)