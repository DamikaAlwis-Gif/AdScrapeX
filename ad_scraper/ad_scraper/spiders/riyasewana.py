import scrapy
from scrapy_playwright.page import PageMethod

class RiyasewanaSpider(scrapy.Spider):
    name = "riyasewana"
    allowed_domains = ["riyasewana.com"]
    start_urls = ["https://riyasewana.com/search/vans"]

    custom_settings = {
        "FEEDS": {
            "output/%(name)s_%(time)s.json": {
                "format": "json",
                "overwrite": True,
            }
        },
        "PLAYWRIGHT_LAUNCH_OPTIONS": {
            "headless": False,  # Set this to True if you want headless mode
        },
        # "PLAYWRIGHT_ABORT_REQUEST": should_abort_request,

    }

    def start_requests(self):
        url = self.start_urls[-1]
        yield scrapy.Request(
            url=url,
            callback=self.parse,
            meta= {
                "playwright": True
            }
        )

    def parse(self, response):
        self.logger.info(f"Parsing {response.url}")
        ad_urls = response.xpath(
            "//ul/li[contains(@class,'item')]/h2[contains(@class,'more')]/a/@href").getall()
        for ad_url in ad_urls:
            yield scrapy.Request(
                url=ad_url,
                callback=self.parse_ad,
                meta={
                    "ad_url": ad_url,
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod(
                            "wait_for_selector", "//div[@id='content']")
                    ],
                }
            )

    def parse_ad(self, response):
        self.logger.info(f"Parsing ad: {response.url}")

        ad_title = response.xpath("//div[@id='content']/h1/text()").get()
        ad_meta_data = response.xpath("//div[@id='content']/h1/following-sibling::h2[1]/text()").get()

        # ad_content_table_rows = response.xpath("//tbody//tr/td//text()").getall()
        # for row in ad_content_table_rows:
        #     if len(row.xpath("/td//p[contains(@class,'moreh')]")) > 0:

        yield {
            "ad_title": ad_title,
            "ad_meta_data": ad_meta_data,
            "ad_url": response.meta['ad_url']
        }


            




