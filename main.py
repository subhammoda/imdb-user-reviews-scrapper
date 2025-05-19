from scraper import IMDBScrapper

movie_urls = ['https://www.imdb.com/title/tt1745960/reviews/?ref_=tt_ql_urv']
ws = IMDBScrapper(movie_urls)
ws.upadate_page_limit(3)
data = ws.get_reviews()
if not data.empty:
    print(data)
    data.to_csv('/movie_reviews.csv')