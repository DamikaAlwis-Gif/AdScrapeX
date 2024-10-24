import scrapy
from scrapy_playwright.page import PageMethod
from urllib.parse import parse_qs, urlencode, urljoin, urlparse


class IkmanSpider(scrapy.Spider):
    name = "ikman"
    allowed_domains = ["ikman.lk"]
    start_urls = ["https://ikman.lk/en/ads/sri-lanka/three-wheelers",
                  "https://ikman.lk/en/ads/sri-lanka/three-wheelers?sort=date&order=desc&buy_now=0&urgent=0&page=18",
                  "https://ikman.lk/en/ads/sri-lanka/lorries",
                  "https://ikman.lk/en/ads/sri-lanka/heavy-duty?page=3",
                  "https://ikman.lk/en/ads/sri-lanka/tractors?page=2",
                  "https://ikman.lk/en/ads/sri-lanka/bicycles?sort=date&order=desc&buy_now=0&urgent=0&page=64",
                  "https://ikman.lk/en/ads/sri-lanka/buses",
                  "https://ikman.lk/en/ads/sri-lanka/land-for-sale",
                  "https://ikman.lk/en/ads/sri-lanka/cars?page=6",
                  "https://ikman.lk/en/ads/sri-lanka/land-for-sale?sort=date&order=desc&buy_now=0&urgent=0&page=80",
                  "https://ikman.lk/en/ads/sri-lanka/apartments-for-sale?sort=date&order=desc&buy_now=0&urgent=0&page=56",
                  "https://ikman.lk/en/ads/sri-lanka/apartment-rentals?sort=date&order=desc&buy_now=0&urgent=0&page=18",
                  "https://ikman.lk/en/ads/sri-lanka/house-rentals?sort=date&order=desc&buy_now=0&urgent=0&page=5"
                  ]

    # three wheel page 100 to go
    # heavy duty done
    # tractors 
    # land for sale 140 to go
    async def should_abort_request(request):
        if request.resource_type in [ "media", "font"]:
            return True
        return False

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
        "PLAYWRIGHT_ABORT_REQUEST": should_abort_request,

    }

    def start_requests(self):
        url = self.start_urls[-1]
        yield scrapy.Request(
            url=url,
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod(
                        "wait_for_selector", "//div[contains(@class, 'ad-list-container')]//ul[contains(@class, 'list')]")
                ],
                # "playwright_include_page": True,
            },
            callback=self.parse
        )

    def parse(self, response):
        self.logger.info(f"Parsing {response.url}")
        # page = response.meta["playwright_page"]

    
        ad_items = response.xpath( 
            "//div[contains(@class, 'ad-list-container')]//ul[contains(@class, 'list')]//li")
        self.logger.info(f"Found {len(ad_items)} ads")

        for ad_item in ad_items:
            ad_url = ad_item.xpath(
                ".//a[contains(@class, 'card-link')]/@href").get()
            
            if ad_url:
                ad_url = urljoin(response.url, ad_url)
                self.logger.info(f"Found ad URL: {ad_url}")

                yield scrapy.Request(
                    url=ad_url,
                    callback=self.parse_ad,
                    meta={
                        "playwright": True,
                        "playwright_page_methods": [
                            PageMethod("wait_for_selector", "//div[contains(@class, 'details-section')]"),
                            # PageMethod("wait_for_selector", "//div[contains(@class, 'gallery')]//img"),
                        ],
                        # "playwright_include_page": True,
                    }
                )
        current_url = response.url
        parsed_url = urlparse(current_url)
        query_params = parse_qs(parsed_url.query)

        # determine the current page number
        page_number = int(query_params.get("page", [1])[0])
        next_page_number = page_number + 1

        # construct the next page URL
        new_query_params = query_params.copy()
        new_query_params["page"] = [next_page_number]

        new_query = urlencode(new_query_params, doseq=True)
        new_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{new_query}"

        self.logger.info(f"Next page URL: {new_url}")

        yield scrapy.Request(
            url=new_url,
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "//div[contains(@class, 'ad-list-container')]//ul[contains(@class, 'list')]")
                ],
                
                # "playwright_include_page": True,
            },
            callback=self.parse,
            errback= self.error_handler
        )




        
        

    def parse_ad(self, response):
        
        # Parse individual ad details
        self.logger.info(f"Parsing ad {response.url}")
        ad_title = response.xpath(
            "//h1[contains(@class, 'title')]/text()").get()
        sub_title = response.xpath(
            "//span[contains(@class, 'sub-title')]/div[contains(@class,'subtitle-wrapper')]/div[1]//text()").getall()
        price = response.xpath(
            "//div[contains(@class, 'price-section')]//text()").getall()
        ad_attributes = response.xpath(
            "//div[contains(@class, 'ad-meta')]//text()").getall()
        ad_description = response.xpath(
            "//div[contains(@class, 'description-section')]//text()").getall()
        image_urls = response.xpath("//div[contains(@class,'gallery')]//img/@src").getall()
        breadcrumbs = response.xpath("//div[contains(@class, 'bread-crumb-wrapper')]//li//text()").getall()

        yield {
            "title": ad_title,
            "sub_title": sub_title,
            "price": price,
            "attributes": ad_attributes,
            "description": ad_description,
            "url": response.url,
            "image_urls": image_urls,
            "breadcrumbs": breadcrumbs
        }

    def error_handler(self, failure):
        self.logger.error(f"An error occurred: {failure}")
        request = failure.request
        self.logger.error(f"Request URL: {request.url}")
        


  # while True:
        #     # Extract ads using Playwright
        #     # content = await page.content()
        #     # selector = scrapy.Selector(text=content)
        #     # ad_items = selector.xpath("//div[contains(@class, 'ad-list-container')]//ul[contains(@class, 'list')]//li")
        #     ad_items = await page.query_selector_all("//div[contains(@class, 'ad-list-container')]//ul[contains(@class, 'list')]//li")
        #     ad_urls = []
        #     for ad_item in ad_items:

        #         await ad_item.click()
        #         print(f"page url: {page.url}")

        #         # ad_url = ad_item.xpath(
        #         #     ".//a[contains(@class, 'card-link')]/@href").get()
        #         # if ad_url:
        #         #     ad_url = urljoin(response.url, ad_url)
        #         #     self.logger.info(f"Found ad URL: {ad_url}")

        #         #     yield scrapy.Request(
        #         #         url=ad_url,
        #         #         callback=self.parse_ad,
        #         #         # meta={
        #         #         #     "playwright": True,
        #         #         #     "playwright_page_methods": [
        #         #         #         PageMethod("wait_for_selector", "//div[contains(@class, 'details-section')]")
        #         #         #     ],
        #         #         #     "playwright_include_page": True,
        #         #         # }
        #         #     )

        #         # await ad_item.click()
        #         # await page.wait_for_selector("//div[contains(@class, 'details-section')]")
        #         # print(f"page url: {page.url}")
        #         # await page.close()

        #     # Handle pagination: Click the "Next" button using Playwright
        #     next_button = await page.query_selector("//div[contains(@class, 'pagination')]//li[contains(@class, 'nextButton')]/a")

        #     if next_button:
        #         self.logger.info("Clicking the next page button...")
        #         await next_button.click()

        #         # Wait for the next page of ads to load
        #         await page.wait_for_selector("//div[contains(@class, 'ad-list-container')]//ul[contains(@class, 'list')]")

        #     else:
        #         self.logger.info("No more pages to load.")
        #         break

        # await page.close()

    # async def parse(self, response):
    #     self.logger.info(f"Parsing {response.url}")

    #     ad_items = response.xpath(
    #         "//div[contains(@class, 'ad-list-container')]//ul[contains(@class, 'list')]//li")

    #     for ad_item in ad_items:
    #         ad_url = ad_item.xpath(
    #             ".//a[contains(@class, 'card-link')]/@href").get()
    #         if ad_url:
    #             ad_url = urljoin(response.url, ad_url)
    #             self.logger.info(f"Found ad URL: {ad_url}")

    #             yield scrapy.Request(
    #                 url=ad_url,
    #                 callback=self.parse_ad,
    #                 # meta={
    #                 #     "playwright": True,
    #                 #     "playwright_page_methods": [
    #                 #         PageMethod("wait_for_selector", "//div[contains(@class, 'details-section')]")
    #                 #     ],
    #                 #     "playwright_include_page": True,
    #                 # }
    #             )

    #     page = response.meta["playwright_page"]

    #     next_button = await page.query_selector("//div[contains(@class, 'pagination')]//li[contains(@class, 'nextButton')]/a")
    #     if next_button:
    #         self.logger.info("Clicking the next page button...")
    #         await next_button.click()
    #         url = page.url
    #         await page.close()

    #         yield scrapy.Request(
    #             url=url,
    #             meta={
    #                 "playwright": True,
    #                 "playwright_page_methods": [
    #                     PageMethod("wait_for_selector", "//div[contains(@class, 'ad-list-container')]//ul[contains(@class, 'list')]")
    #                 ],
    #                 "playwright_include_page": True,
    #             },
    #             callback=self.parse
    #         )
