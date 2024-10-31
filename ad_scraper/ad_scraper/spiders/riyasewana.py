import scrapy


class RiyasewanaSpider(scrapy.Spider):
    name = "riyasewana"
    allowed_domains = ["riyasewana.com"]
    start_urls = ["https://riyasewana.com"]

    def parse(self, response):
        self.logger.info(f"Parsing {response.url}")

        pass
