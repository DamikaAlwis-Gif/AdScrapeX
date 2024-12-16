import scrapy
from scrapy_playwright.page import PageMethod
from ..utils import genaral
from urllib.parse import urljoin
import time
import random

class RiyasewanaSpider(scrapy.Spider):
    name = "riyasewana"
    allowed_domains = ["riyasewana.com"]
    start_urls = ["https://riyasewana.com/search/suvs"]

    custom_settings = {
        "FEEDS": {
            "output/%(name)s_%(time)s.json": {
                "format": "json",
                "overwrite": True,
            }
        },
        # "PLAYWRIGHT_LAUNCH_OPTIONS": {
        #     "headless": False,  # Set this to True if you want headless mode
        # },
        "PLAYWRIGHT_ABORT_REQUEST": genaral.should_abort_request,
        "JOBDIR": "job_data/riyasewana_job",
        "DOWNLOAD_DELAY": random.uniform(1, 3), 

    }

        # List of user agents to rotate
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        # Add more user agents as needed
    ]


    def start_requests(self):
        url = self.start_urls[-1]
        yield scrapy.Request(
            url=url,
            callback=self.parse,
            headers={'User-Agent': random.choice(self.user_agents)},
            meta= {
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod(
                        "wait_for_selector", "//ul/li[contains(@class,'item')]")
                ],
            }
        )
        time.sleep(random.uniform(1, 3))

    async def parse(self, response):
        self.logger.info(f"Parsing {response.url}")
        ad_urls = response.xpath(
            "//ul/li[contains(@class,'item')]/h2[contains(@class,'more')]/a/@href").getall()
        for ad_url in ad_urls:
            yield scrapy.Request(
                url=ad_url,
                callback=self.parse_ad,
                headers={'User-Agent': random.choice(self.user_agents)},
                meta={
                    "ad_url": ad_url,
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod(
                            "wait_for_selector", "//div[@id='content']", timeout=60000)
                    ],
                }
            )
        next_page_url = response.xpath("//div[@class='pagination']//a[contains(text(), 'Next')][last()]/@href").get()
        if next_page_url:
            yield scrapy.Request(
                url= urljoin("https:",next_page_url),
                callback=self.parse,
                headers={'User-Agent': random.choice(self.user_agents)},
                meta= {
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod(
                            "wait_for_selector", "//ul/li[contains(@class,'item')]")
                    ],
                }
            )

    def parse_ad(self, response):
        self.logger.info(f"Parsing ad: {response.url}")

        ad_title = response.xpath("//div[@id='content']/h1/text()").get()
        ad_meta_data = response.xpath("//div[@id='content']/h1/following-sibling::h2[1]/text()").get()

        # ad_content = response.xpath("//tbody//tr/td//text()").getall()
        ad_content = []
        table_rows = response.xpath("//tbody//tr")
        for row in table_rows:
            if len(row.xpath("./td//p[contains(@class,'moreh')]")) > 0:
                ad_content += row.xpath(".//td//text()").getall()
        ad_content = [text.strip() for text in ad_content if text.strip()]
        yield {
            "ad_title": ad_title,
            "ad_meta_data": ad_meta_data,
            "ad_url": response.meta['ad_url'],
            "ad_content": ad_content
        }


            




