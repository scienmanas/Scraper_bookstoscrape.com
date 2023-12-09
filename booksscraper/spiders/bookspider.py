from typing import Iterable
import scrapy
import random

from scrapy.http import Request
from booksscraper.items import BookItem
from urllib.parse import urlencode


# def get_proxy_url(url) :
#     payload = {
#         'api_key' : API_KEY,
#         'url' : url,
#         'residential' : 'true'
#     }
#     proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
#     return proxy_url

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com", 'proxy.scrapeops.io']
    start_urls = ["https://books.toscrape.com/"]

    # Overwite setting in setting file
    custom_settings = {
        'FEEDS' : { 
            'booksdata_clean_customsetting.json' : {'format': 'json' , 'overwrite': True},
        },
    }

    def start_requests(self) :
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse)
    
    def __init__(self) :
        # self.user_agent_list = {
        #     'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
        #     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        #     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        #     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        #     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        #     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
        #     'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
        # }
        pass

    def parse(self, response):
        books = response.css('article.product_pod')
        # Loop to every book in that page
        for book in books :
            # Scrape indivudual book data
            relative_url_book = book.css('h3 a ::attr(href)').get()

            if 'catalogue/' in relative_url_book :
                book_url = "https://books.toscrape.com/" + relative_url_book
            else :
                book_url = "https://books.toscrape.com/catalogue/" + relative_url_book
            # yield response.follow(book_url, callback=self.parse_book_page)
            yield scrapy.Request(url=book_url, callback=self.parse_book_page)

    
        # To move to next page
        next_page = response.css('li.next a::attr(href)').get()

        if next_page is not None :
            if 'catalogue/' in next_page :
                next_page_url = "https://books.toscrape.com/" + next_page
            else :
                next_page_url = "https://books.toscrape.com/catalogue/" + next_page
            # yield response.follow(next_page_url, callback= self.parse, headers={"User-Agent": random.choice(self.user_agent_list)})
            # yield response.follow(next_page_url, callback= self.parse)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_book_page(self, response) :
        # Got the html stored in the response once we do response.follow
        # Scrapping through the table rows
        table_rows = response.css('table tr')
        book_item = BookItem()

        # yield {
        #     'url' : response.url,
        #     'title' : response.css('.product_main h1::text').get(),
        #     'product_type' : table_rows[1].css('td ::text').get(),
        #     'upc' : table_rows[0].css('td ::text').get(),
        #     'price_excl_tax' : table_rows[2].css('td ::text').get(),
        #     'price_incl_tax' : table_rows[3].css('td ::text').get(),
        #     'tax' : table_rows[4].css('td ::text').get(),
        #     'availability' : response.css('p.availability').xpath('string()').get().strip(),
        #     'num_reviews' : table_rows[6].css('td ::text').get(),
        #     'stars' : response.css('p.star-rating').attrib['class'].split(' ')[1],
        #     'category' : response.xpath("/html/body/div/div/ul/li[3]/a/text()").get(),
        #     'description' : response.xpath("/html/body/div/div/div[2]/div[2]/article/p/text()").get(),
        #     'price' : response.css('p.price_color ::text').get(),
        # }

        book_item['url'] = response.url
        book_item['title'] = response.css('.product_main h1::text').get()
        book_item['upc'] = table_rows[0].css('td ::text').get()
        book_item['product_type'] = table_rows[1].css('td ::text').get()
        book_item['price_excl_tax'] = table_rows[2].css('td ::text').get()
        book_item['price_incl_tax'] = table_rows[3].css('td ::text').get()
        book_item['tax'] = table_rows[4].css('td ::text').get()
        book_item['availability'] = table_rows[5].css("td ::text").get()
        book_item['num_reviews'] = table_rows[6].css('td ::text').get()
        book_item['stars'] = response.css('p.star-rating').attrib['class'].split(' ')[1]
        book_item['category'] = response.xpath("/html/body/div/div/ul/li[3]/a/text()").get()
        book_item['description'] = response.xpath("/html/body/div/div/div[2]/div[2]/article/p/text()").get()
        book_item['price'] = response.css('p.price_color ::text').get()

        yield book_item