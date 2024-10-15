from typing import Iterable
import scrapy
from scrapy_playwright.page import PageMethod

class IkmanSpider(scrapy.Spider):
    name = "ikman"
    allowed_domains = ["ikman.lk"]
    start_urls = ["https://ikman.lk",
                  "https://ikman.lk/en/ads/sri-lanka/three-wheelers"]
    
    custom_settings = {

        # "PLAYWRIGHT_ABORT_REQUEST": should_abort_request,
        "FEEDS": {
            "output/%(name)s_%(time)s.json": {
                "format": "json",
                "overwrite": True,

            }
        },

        # "PLAYWRIGHT_LAUNCH_OPTIONS": {
        #     "headless": False,
        # }

    }

    
    def start_requests(self):
        url = self.start_urls[1]
        yield scrapy.Request(
            url=self.encode_url(url),
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "//div[contains(@class, 'ad-list-container')]//ul[contains(@class, 'list')]")
                ],
                # "playwright_include_page": True,
            }
        )

    
    def parse(self, response):
        self.logger.info(f"Parsing {response.url}")
        ad_items = response.xpath("//div[contains(@class, 'ad-list-container')]//ul[contains(@class, 'list')]//li")
        
        for ad_item  in ad_items:
            ad_url = ad_item.xpath(".//a[contains(@class, 'card-link')]/@href").get()
            ad_title = ad_item.xpath(".//a[contains(@class, 'card-link')]/@title").get()

            yield scrapy.Request(
                url = response.urljoin(ad_url),
                callback = self.parse_ad,
                )


    def parse_ad(self, response):
        self.logger.info(f"Parsing ad {response.url}")
        ad_title = response.xpath("//h1[contains(@class, 'title')]/text()").get()
        sub_title = response.xpath("//span[contains(@class, 'sub-title')]/div[contains(@class,'subtitle-wrapper')]/div[1]//text()").getall()
        price = response.xpath("//div[contains(@class, 'price-section')]//text()").getall()
        ad_attributes = response.xpath("//div[contains(@class, 'ad-meta')]//text()").getall()
        ad_description = response.xpath("//div[contains(@class, 'description-section')]//text()").getall()
        # image_urls = response.xpath("//div[contains(@class,'gallery')]//img/@src").getall()
        yield {
            "title": ad_title,
            "sub_title": sub_title,
            "price": price,
            "attributes": ad_attributes,
            "description": ad_description,
            "url": response.url,
            # "image_urls": image_urls

        }

        
