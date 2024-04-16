# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import pymongo
import sqlite3


class MongodbPipeline:

    collection_name = "best_movies"

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(
            "mongodb+srv://biruh:testtest@cluster0.g8xkheh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        )
        self.db = self.client["IMDB"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(item)
        return item


class SQLlitePipeline:

    def open_spider(self, spider):
        self.connection = sqlite3.connect("imdb.db")
        self.c = self.connection.cursor()
        try:
            self.c.execute(
                """
                CREATE TABLE best_movies(
                    title TEXT,
                    year TEXT,
                    duration TEXT,
                    genere TEXT,
                    rating TEXT,
                    movie_url TEXT
                )
            """
            )
            self.connection.commit()
        except sqlite3.OperationalError:
            pass

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.c.execute(
            """
           INSERT INTO best_movies(title, year, duration, genere, rating, movie_url) VALUES (?,?,?,?,?,?) 
        """,
            (
                item["header"],
                item["year"],
                item["duration"],
                item["genere"],
                item["rating"],
                item["movie_url"],
            ),
        )
        self.connection.commit()

        return item
