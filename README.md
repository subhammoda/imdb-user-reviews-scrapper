
# IMDb User Reviews Scraper

## Overview

This Python script automates the extraction of user reviews for movies listed on IMDb. By leveraging Selenium and BeautifulSoup, it navigates through IMDb pages to gather user-generated reviews, which can be valuable for sentiment analysis, research, or other analytical purposes.

## Features

- Scrapes user reviews from IMDb movie pages.
- Stores extracted reviews in a structured format (e.g., CSV or JSON).
- Handles dynamic content loading using Selenium.
- Parses HTML content efficiently with BeautifulSoup.

## Prerequisites

Before using this script, ensure you have the following installed:

- **Python 3.12 or higher**
- **Google Chrome Browser**
- **Chrome WebDriver**: Compatible with your Chrome browser version. [Download here](https://chromedriver.chromium.org/downloads).

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/subhammoda/imdb-user-reviews-scrapper.git
   cd imdb-user-reviews-scrapper
   ```

2. **Create and activate a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the required Python packages:**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Set the path to your Chrome WebDriver:**

   In the `scraper.py` script, locate the section where the WebDriver is initialized and update the path:

   ```python
   driver = webdriver.Chrome(executable_path='/path/to/chromedriver')
   ```

   Replace `'/path/to/chromedriver'` with the actual path to your downloaded Chrome WebDriver.

2. **Specify the IMDb movie URL:**

   Update the `main.py` script to include the IMDb URL of the user reviews page of the movie/movies you wish to scrape reviews from. For example:

   ```python
   movie_url = ['https://www.imdb.com/title/tt0111161/reviews/?ref_=tt_ov_ql_2']  # The Shawshank Redemption
   ```

## Usage

Run the script using the following command:

```bash
python main.py
```

The script will:

- Navigate to the specified IMDb movie page.
- Extract user reviews.
- Save the reviews to as a dataframe, which you can further download or store in required format.

## Output

The extracted reviews will be saved in the project directory, typically in a file named `movie_reviews.csv`.

## Notes

- Ensure that the Chrome WebDriver version matches your installed Chrome browser version to avoid compatibility issues.
- IMDb's website structure may change over time. If the script encounters errors, inspect the website's HTML structure and update the selectors in the script accordingly.
- Always respect IMDb's [Terms of Use](https://www.imdb.com/conditions) when scraping data.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Selenium](https://www.selenium.dev/) for browser automation.
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing.