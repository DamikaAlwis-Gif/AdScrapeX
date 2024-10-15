import scrapy
from scrapy_playwright.page import PageMethod
from urllib.parse import quote
class PatpatSpider(scrapy.Spider):
    name = "patpat"
    allowed_domains = ["patpat.lk"]
    start_urls = ["https://patpat.lk",
                  "https://patpat.lk/marketplace/all-sri-lanka/all-cities/Electronics/newest",
                  "https://www.patpat.lk/marketplace/all-sri-lanka/all-cities/Home-&-Living/newest",
                  "https://www.patpat.lk/marketplace/all-sri-lanka/all-cities/Pets/newest",
                  "https://www.patpat.lk/marketplace/all-sri-lanka/all-cities/Automotive/newest",
                  "https://www.patpat.lk/marketplace/all-sri-lanka/all-cities/Fashion-&-Accessories/newest",
                  "https://www.patpat.lk/marketplace/all-sri-lanka/all-cities/Businesses-&-Industries/newest",
                  "https://www.patpat.lk/marketplace/all-sri-lanka/all-cities/Services/newest",
                  "https://www.patpat.lk/marketplace/all-sri-lanka/all-cities/Hobbies,-Sports-&-Fitness/newest",
                  "https://www.patpat.lk/marketplace/all-sri-lanka/all-cities/Health/newest",]

    async def should_abort_request(request):
        if request.resource_type in ["image", "media", "font"]:
            return True
        return False
    
    def encode_url(self,url):
        return quote(url, safe=":/?=&")


    custom_settings = {

        "PLAYWRIGHT_ABORT_REQUEST": should_abort_request,
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
        url = self.start_urls[9]
        yield scrapy.Request(
            url = self.encode_url(url),
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", ".marketplace-list-view")
                ],
                # "playwright_include_page": True,    
            }
        )

    async def parse(self, response):
        self.logger.info(f"Parsing {response.url}")
        ad_items = response.css(".result-item")
        self.logger.info(f"Found {len(ad_items)} ads")

        for ad_item in ad_items:

            ad_title = ad_item.css("h4.card-title a")
            ad_url = ad_title.attrib.get("href")
           
            yield scrapy.Request(
                url = self.encode_url(ad_url),  
                callback=self.parse_ad,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", ".item-preview")
                    ],
                    
                }
            )
            next_page_link = response.css("li.page-item a.page-link[rel='next'] ::attr(href)").get()

            if next_page_link:
                yield response.follow(
                    url = self.encode_url(next_page_link),
                    callback=self.parse,
                    meta={
                        "playwright": True,
                        "playwright_page_methods": [
                            PageMethod("wait_for_selector", ".marketplace-list-view")
                        ],
                    }
                )




    async def parse_ad(self, response):
        self.logger.info(f"Parsing ad {response.url}")
        ad_title = response.css("h2.item-title ::text").get()
        marketplace_item_info = response.css("div.marketplace-item-info")

        price = marketplace_item_info.css(".item-price ::text").getall()
        cleaned_price = " ".join([item.strip() for item in price if item.strip()])

        info_table = marketplace_item_info.css("table.course-info")
        ad_attributes = info_table.css("::text").getall()
        cleaned_ad_attributes = [item.strip() for item in ad_attributes if item.strip()] 

        ad_description = response.css("div.item-description p ::text").getall()
        cleaned_ad_description = [item.strip() for item in ad_description if item.strip()]

        img_urls = response.css("div.item-images img::attr(src)").getall()

        yield {
            "ad_title": ad_title,
            "price": cleaned_price,
            "ad_attributes": cleaned_ad_attributes,
            "ad_description": cleaned_ad_description,
            "ad_url": response.url,
            "img_urls": img_urls
        }








        
        
