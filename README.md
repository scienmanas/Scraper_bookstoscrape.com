# Scrapy Spider bookstoscrape.com
This repository contains codes which I wrote during learning Scrapy by building a spider to scrap data from Books To Scrap Website

## Scrapped Wesbite 
Wesbite: [Books to Scrape](https://books.toscrape.com/)

## How to run

### Running locally 

1. Clone the repository
```
git clone https://github.com/scienmanas/Scraper_bookstoscrape.com.git
```
2. Install the requirements
```
pip install -r requirements.txt
```
3. Run the spider
```
scrapy crawl bookspider
```
### Running on Scrapy Cloud

1. Create a new Scrapy Cloud project
2. Deploy the project
```
shub deploy
```
3. Run the spiderpider
```
shub crawl books
```
## Purpose 

The purpose of this repository is to learn Scrapy and to help others who are learning Scrapy.

The webiste scraped is open to scrapping to individuals to learn and test we scrapping

## Technologies Used

1. The Project uses ScrapeOps APIs for proxies, handling headers and user agents .
2. The Website can be accessed by the link : https://scrapeops.io/
