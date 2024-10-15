# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AdScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ad_title = scrapy.Field()
    breadcrumbs = scrapy.Field()
    more_details = scrapy.Field()
    features = scrapy.Field()
    description = scrapy.Field()
    date_time = scrapy.Field()
    ad_url = scrapy.Field()
    images_urls = scrapy.Field()

    
