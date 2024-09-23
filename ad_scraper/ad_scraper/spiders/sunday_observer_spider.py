import scrapy


class SundayObserverSpiderSpider(scrapy.Spider):
    name = "sunday_observer_spider"
    allowed_domains = ["sundayobserver.lk"]
    start_urls = ["https://sundayobserver.lk/classifieds/"]

    def parse(self, response):

        # with open('sunday_observer_classifieds.html', 'w', encoding='utf-8') as f:
        #     f.write(response.text)

        # # Optionally, you can also log or print the HTML content
        # self.log("HTML content saved to sunday_observer_classifieds.html")
        pass
        
