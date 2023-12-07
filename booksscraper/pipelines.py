# Define your item pipelines here
# Use it to clean the data
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import mysql.connector
from itemadapter import ItemAdapter


class BooksscraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        # Strip all the whitespaces for the strings
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value.strip()

        # Category & Product Types --> switch to lowercase
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()

        # Price --> conversion and cleaning
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£', '')
            adapter[price_key] = float(value)

        # Availability of books - only extract numbers
        availability_string = adapter.get('availability')
        if 'In stock' in availability_string:
            adapter['availability'] = int(
                availability_string.split('(')[1].split(' ')[0])
        else:
            adapter['availability'] = int(0)

        # Reviews --> To integer
        num_reviews_string = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews_string)

        # Turn stars Rating into integers
        stars_string = adapter.get('stars')
        stars_text_value = stars_string.lower()
        if stars_text_value == 'zero':
            adapter['stars'] = 0
        elif stars_text_value == 'one':
            adapter['stars'] = 1
        elif stars_text_value == 'two':
            adapter['stars'] = 2
        elif stars_text_value == 'three':
            adapter['stars'] = 3
        elif stars_text_value == "four":
            adapter['stars'] = 4
        elif stars_text_value == 'five':
            adapter['stars'] = 5

        return item


class SaveToMySQLPipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='books',
        )

        # Create cursor used to execute commands
        self.cursor = self.conn.cursor()

        # create books table if not exists
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS books(
            id int NOT NULL auto_increment,
            url VARCHAR(255),
            title text,
            upc VARCHAR(255),
            product_type VARCHAR(255),
            price_excl_tax DECIMAL,
            price_incl_tax DECIMAL,
            tax DECIMAL,
            price DECIMAL,
            availability INTEGER,
            num_reviews INTEGER,
            stars INTEGER,
            category VARCHAR(255),
            description text,
            PRIMARY KEY (id)
            )
        """)
    def process_item(self, item, spider) :
        
        ## Define insert statement
        self.cursor.execute(""" insert into books (
                url,
                title,           
                upc,
                product_type,
                price_excl_tax,
                price_incl_tax,
                tax,
                price,
                availability,
                num_reviews,
                stars,
                category,
                description
            ) values (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )""" , (
            item['url'],
            item['title'],
            item['upc'],
            item['product_type'],
            item['price_excl_tax'],
            item['price_incl_tax'],
            item['tax'],
            item['price'],
            item['availability'],
            item['num_reviews'],
            item['stars'],
            item['category'],
            item['description']
            )
        )

        ## Execute insert into the database
        self.conn.commit()
        return item
    
    def close_spider(self, spider) :
        self.cursor.close()
        self.conn.close()