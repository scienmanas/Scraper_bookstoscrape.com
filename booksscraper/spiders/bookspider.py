import scrapy
from booksscraper.items import BookItem

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    # Overwite setting in setting file
    custom_settings = {
        'FEEDS' : { 
            'booksdata_clean_customsetting.json' : {'format': 'json' , 'overwrite': True},
        },
    }

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
            yield response.follow(book_url, callback=self.parse_book_page)
    
        # To move to next page
        next_page = response.css('li.next a::attr(href)').get()

        if next_page is not None :
            if 'catalogue/' in next_page :
                next_page_url = "https://books.toscrape.com/" + next_page
            else :
                next_page_url = "https://books.toscrape.com/catalogue/" + next_page
            yield response.follow(next_page_url, callback= self.parse)

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