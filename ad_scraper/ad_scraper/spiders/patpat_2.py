import scrapy
from scrapy_playwright.page import PageMethod
from urllib.parse import quote

class Patpat2Spider(scrapy.Spider):
    name = "patpat_2"
    allowed_domains = ["patpat.lk"]
    start_urls = ["https://patpat.lk", "https://www.patpat.lk/vehicle",
                  "https://www.patpat.lk/vehicle?page=298&city=&sub_category=&sub_category_name=&category=vehicle&search_txt=&sort_by=",
                  "https://www.patpat.lk/property",
                  "https://www.patpat.lk/property?page=365&city=&sub_category=&sub_category_name=&category=property&search_txt=&sort_by=",
                  "https://www.patpat.lk/vehicle/filter/three_wheeler",
                  "https://www.patpat.lk/vehicle/filter/bike",
                  "https://www.patpat.lk/vehicle/filter/bike?page=151&city=&sub_category=bike&sub_category_name=Motorbikes&category=vehicle&search_txt=&sort_by=",
                  "https://www.patpat.lk/vehicle/filter/truck",
                  "https://www.patpat.lk/vehicle/filter/van?page=62&city=&sub_category=van&sub_category_name=Vans&category=vehicle&search_txt=&sort_by=",
                  "https://www.patpat.lk/vehicle/filter/three_wheeler?page=42&city=&sub_category=three_wheeler&sub_category_name=Three%20Wheelers&category=vehicle&search_txt=&sort_by=",
                  "https://www.patpat.lk/property?page=800&city=&sub_category=&sub_category_name=&category=property&search_txt=&sort_by="]
    # vehicle page page 410 to go
    # property page 365 to go
    # bike page 151 to go
    # van done
    # truck done
    # property done
    # three wheel page 175 to go
    async def should_abort_request(request):
        if request.resource_type in ["image", "media", "font"]:
            return True
        return False

    def encode_url(self, url):
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
        url = self.start_urls[11]
        yield scrapy.Request(
            url=self.encode_url(url),
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", ".itemlist")
                    # PageMethod("wait_for_selector", ".item-list")
                ],
                # "playwright_include_page": True,
            }
        )

    async def parse(self, response):

        self.logger.info(f"Parsing {response.url}")

        ad_items = response.css(".result-item")

        self.logger.info(f"Found {len(ad_items)} ads")

        for ad_item in ad_items:

            
            ad_url = ad_item.css(".course-info a::attr(href)").get()

            yield scrapy.Request(
                url=self.encode_url(ad_url),
                callback=self.parse_ad,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", ".item-preview")
                    ],

                }
            )
            next_page_link = response.css(
                "li.page-item a.page-link[rel='next'] ::attr(href)").get()

            if next_page_link:
                yield response.follow(
                    url=self.encode_url(next_page_link),
                    callback=self.parse,
                    meta={
                        "playwright": True,
                        "playwright_page_methods": [
                            PageMethod("wait_for_selector",
                                       ".itemlist", timeout=60000, state="visible")
                        ],
                       
                    }
                )

    async def parse_ad(self, response):
        self.logger.info(f"Parsing ad {response.url}")

        ad_title = response.css("h2.item-title ::text").get()
        marketplace_item_info = response.css("div.item-info")

        price = marketplace_item_info.css(".item-price ::text").getall()
        cleaned_price = " ".join([item.strip()
                                 for item in price if item.strip()])

        info_table = marketplace_item_info.css("table.course-info")
        ad_attributes = info_table.css("::text").getall()
        cleaned_ad_attributes = [item.strip()
                                 for item in ad_attributes if item.strip()]

        ad_description = response.css("div.item-description p ::text").getall()
        cleaned_ad_description = [item.strip()
                                  for item in ad_description if item.strip()]

        img_urls = response.css("div.item-images img::attr(src)").getall()

        yield {
            "ad_title": ad_title,
            "price": cleaned_price,
            "ad_attributes": cleaned_ad_attributes,
            "ad_description": cleaned_ad_description,
            "ad_url": response.url,
            "img_urls": img_urls
        }
