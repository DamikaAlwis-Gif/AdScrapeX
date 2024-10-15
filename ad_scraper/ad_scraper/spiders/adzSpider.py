# from typing import Iterable
# import scrapy
# from scrapy_playwright.page import PageMethod
import re
# class AdzSpider(scrapy.Spider):
#     name = "adzSpider"
#     allowed_domains = ["adz.lk"]
#     start_urls = ["https://adz.lk/ads/"]

#     def start_requests(self):
#         url = self.start_urls[0] 
#         yield scrapy.Request(url , meta= {
#             "playwright": True,
#             "playwright_page_methods": [
#                 PageMethod(
#                     "wait_for_selector",
#                     ".listivo-listing-grid a"
#                 )
#             ]
#         })


#     def parse(self, response):
#         # get all ad links in the current page
#         ad_links = response.css(".listivo-listing-grid a ::attr(href)").getall()
#         # for ad_link in ad_links:
#         #     yield ad_link
#         for ad_link in ad_links:
#             print("***************************** ad_link: ", ad_link)
#             yield response.follow(ad_link, self.parse_ad, 
#                                   meta = {
#                 "playwright": True,
#                 "playwright_page_methods": [
#                     PageMethod(
#                         "wait_for_selector",
#                         ".elementor-column"
#                     )
#                 ]
#             }
#             )
#         # next_page_link = response.css("a.next.page-numbers ::attr(href)").get()    
#         # pass
#         next_button = response.css(
#             "div.listivo-pagination__item:last-child")
#         print("***************************** next button: ", next_button)
#         is_next_disabled = next_button.css("::attr(class)").re(r'--disabled')
#         print("***************************** is_next_disabled: ", is_next_disabled)
#         if len(is_next_disabled) == 0:
#             yield scrapy.Request(
#                 response.url,
#                 meta={
#                     "playwright": True,
#                     "playwright_page_methods": [
#                         PageMethod(
#                             "click",
#                             "div.listivo-pagination__item:last-child"
#                         ),
#                         PageMethod(
#                             "wait_for_selector",
#                             ".elementor-column"
#                         )
#                     ]
#                 }
#             )
        


        
        



#     def parse_ad(self, response):
#         yield{
#             "url": response.url,
#             "title": response.css("h1.listivo-listing-name ::text").get(),
#         }

# from typing import Iterable
# import scrapy
# from scrapy_playwright.page import PageMethod

# class AdzSpider(scrapy.Spider):
#     name = "adzSpider"
#     allowed_domains = ["adz.lk"]
#     start_urls = ["https://adz.lk/ads/"]

#     def start_requests(self):
#         url = self.start_urls[0]
#         yield scrapy.Request(
#             url,
#             meta={
#                 "playwright": True,
#                 "playwright_page_methods": [
#                     PageMethod("wait_for_selector", ".listivo-listing-grid a")
#                 ]
#             }
#         )

#     def parse(self, response):
#         # Get all ad links on the current page
#         ad_links = response.css(".listivo-listing-grid a::attr(href)").getall()
        
#         for ad_link in ad_links:
#             yield response.follow(
#                 ad_link,
#                 self.parse_ad,
#                 meta={
#                     "playwright": True,
#                     "playwright_page_methods": [
#                         PageMethod("wait_for_selector", ".elementor-column")
#                     ]
#                 }
#             )

#         # Find the last pagination button
#         next_button = response.css("div.listivo-pagination__item:last-child")
        
#         # Check if the next button is disabled
#         if not next_button.css("::attr(class)").re(r'--disabled'):
#             # Simulate a click on the next button
#             yield scrapy.Request(
#                 response.url,
#                 meta={
#                     "playwright": True,
#                     "playwright_page_methods": [
#                         PageMethod("click", "div.listivo-pagination__item:last-child"),  # Click the next button
#                         PageMethod("wait_for_selector", ".listivo-listing-grid a")  # Wait for the next page to load
#                     ]
#                 },
#                 callback=self.parse

#             )

#     def parse_ad(self, response):
#         # Scrape ad details from each individual ad page
#         yield {
#             "url": response.url,
#             "title": response.css("h1.listivo-listing-name::text").get(),
#         }


from urllib.parse import urlparse, parse_qs, urlencode
from typing import Iterable
import scrapy
from scrapy_playwright.page import PageMethod

def should_abort_request(request):
    if request.resource_type in ["image", "media", "font"]:
        return True
    return False

# class AdzSpider(scrapy.Spider):
#     name = "adzSpider"
#     allowed_domains = ["adz.lk"]
#     start_urls = ["https://adz.lk/ads/"]

#     custom_settings = {
#         "PLAYWRIGHT_BROWSER_OPTIONS": {
#             "headless": False
#         },
#         "PLAYWRIGHT_ABORT_REQUEST": should_abort_request
#     }

#     def start_requests(self):
#         url = self.start_urls[0]
#         yield scrapy.Request(
#             url,
#             meta={
#                 "playwright": True,
#                 "playwright_include_page": True,
#                 "playwright_page_methods": [
#                     PageMethod("wait_for_selector", ".listivo-listing-grid a")
#                 ]
#             }
#         )

#     async def parse(self, response):
#         # Get all ad links on the current page
#         page = response.meta["playwright_page"]
#         ad_links = response.css(".listivo-listing-grid a::attr(href)").getall()
#         self.logger.info(response.url)

#         for ad_link in ad_links:
#             yield response.follow(
#                 ad_link,
#                 self.parse_ad,
#                 meta={
#                     "playwright": True,
#                     "playwright_include_page": True,
#                     "playwright_page_methods": [
#                         PageMethod("wait_for_selector", ".elementor-column")
#                     ]
#                 }
#             )

#         next_button_element = page.locator(
#             "div.listivo-search-results__pagination-desktop div.listivo-pagination__item:last-child")

#         # Find the last pagination button
#         next_button = response.css(
#             "div.listivo-search-results__pagination-desktop div.listivo-pagination__item:last-child")

#         # Check if the next button is disabled
#         if not next_button.css("::attr(class)").re(r'--disabled'):
            
#             await next_button_element.click()
                
#             new_url = page.url
#             self.logger.info(new_url)
#             yield scrapy.Request(new_url, callback=self.parse, 
#                                  meta={
#                                     "playwright": True,
#                                     "playwright_include_page": True,
#                                     "playwright_page_methods": [
#                                         PageMethod("wait_for_selector", ".listivo-listing-grid a")
#                                     ]
#                                 })

            

#     def parse_ad(self, response):
#         # Scrape ad details from each individual ad page
#         yield {
#             "url": response.url,
#             "title": response.css("h1.listivo-listing-name::text").get(),
#         }

# class AdzSpider(scrapy.Spider):
#     name = "adzSpider"
#     allowed_domains = ["adz.lk"]
#     start_urls = ["https://adz.lk/ads/"]

#     custom_settings = {
#         "PLAYWRIGHT_BROWSER_OPTIONS": {
#             "headless": False
#         },
#         "PLAYWRIGHT_ABORT_REQUEST": should_abort_request
#     }

#     def start_requests(self):
#         url = self.start_urls[0]
#         yield scrapy.Request(
#             url,
#             meta={
#                 "playwright": True,
#                 "playwright_include_page": True,
#                 "playwright_page_methods": [
#                     PageMethod("wait_for_selector", ".listivo-listing-grid a")
#                 ],
#                 "errback": self.errback
#             }
#         )

#     async def parse(self, response):
#         # Get the Playwright page instance
#         page = response.meta["playwright_page"]

#         # Get all ad links on the current page
#         ad_links = response.css(".listivo-listing-grid a::attr(href)").getall()
#         self.logger.info(response.url)

#         for ad_link in ad_links:
#             yield response.follow(
#                 ad_link,
#                 self.parse_ad,
#                 meta={
#                     "playwright": True,
#                     "playwright_include_page": True,
#                     "playwright_page_methods": [
#                         PageMethod("wait_for_selector", ".elementor-column")
#                     ]
#                 }
#             )

#         # Pagination logic
#         next_button_element = page.locator(
#             "div.listivo-search-results__pagination-desktop div.listivo-pagination__item:last-child")

#         next_button = response.css(
#             "div.listivo-search-results__pagination-desktop div.listivo-pagination__item:last-child")

#         self.logger.info(next_button.css("::attr(class)").re(r'--disabled'))
#         # Check if the next button is disabled
#         if not next_button.css("::attr(class)").re(r'--disabled'):
#             await next_button_element.click()
#             new_url = page.url
#             self.logger.info(new_url)
#             # Close the Playwright page
#             await page.close()  # Close the page after scraping

#             yield scrapy.Request(new_url, callback=self.parse,
#                                  meta={
#                                      "playwright": True,
#                                      "playwright_include_page": True,
#                                      "playwright_page_methods": [
#                                          PageMethod(
#                                              "wait_for_selector", ".listivo-listing-grid a")
#                                      ]
#                                  })

        

#     async def parse_ad(self, response):
#         # Scrape ad details from each individual ad page
#         yield {
#             "url": response.url,
#             "title": response.css("h1.listivo-listing-name::text").get(),
#         }

#         # Get the Playwright page instance for the ad page and close it
#         page = response.meta.get("playwright_page")
#         if page:
#             await page.close()  # Close the ad page after scraping

#     async def errback(self, failure):
#         page = failure.request.meta["playwright_page"]
#         await page.close()
# page 376

class AdzSpider(scrapy.Spider):
    name = "adzSpider"
    allowed_domains = ["adz.lk"]
    start_urls = ["https://adz.lk/ads/"," https://adz.lk/ads/?pagination=389&sort-by=most-relevant&view=card"]

    custom_settings = {
                
                "PLAYWRIGHT_ABORT_REQUEST": should_abort_request,
                "FEEDS": {
                    "output/%(name)s_%(time)s.json": {
                        "format": "json",
                        "overwrite": True,

                    }
                },
                
                # "PLAYWRIGHT_LAUNCH_OPTIONS" : {
                # "headless": False,
                # }
                
            }

    def start_requests(self):
        url = self.start_urls[1]
        yield scrapy.Request(
            url,
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", ".listivo-listing-grid a")
                ]
            }
        )

    def parse(self, response):
        # Get all ad links on the current page
        ad_links = response.css(".listivo-listing-grid a::attr(href)").getall()

        for ad_link in ad_links:
            yield response.follow(
                ad_link,
                self.parse_ad,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", ".elementor-column")
                    ]
                }
            )

        # Construct the URL for the next page
        current_url = response.url
        parsed_url = urlparse(current_url)
        query_params = parse_qs(parsed_url.query)

        # Default values for pagination
        current_page = int(query_params.get('pagination', [1])[0])
        next_page = current_page + 1

        # Build new query parameters while keeping existing ones
        new_query_params = {
            'pagination': next_page,
            'sort-by': query_params.get('sort-by', ['most-relevant'])[0],
            'view': query_params.get('view', ['card'])[0]
        }

        # Create the new URL for the next page
        new_query = urlencode(new_query_params, doseq=True)
        next_page_url = f"{
            parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{new_query}"

        # Log the next page URL for debugging
        self.logger.info(f"Next Page URL: {next_page_url}")

        # Yield a request for the next page
        yield scrapy.Request(
            next_page_url,
            callback=self.parse,
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", ".listivo-listing-grid a")
                ]
            }
        )

    def parse_ad(self, response):
        self.logger.info(f"Parsing ad: {response.url}")
        image_urls = response.css(".listivo-gallery-v1 img ::attr(src)").getall()
        attributes = response.css(".listivo-listing-attributes-v3 ::text").getall()
        description = response.css(".listivo-listing-section__text p ::text").getall()
        title = response.css("h1.listivo-listing-name::text").get()
        yield {
            "url": response.url,
            "title": title,
            "images": image_urls,
            "attributes": attributes,
            "description": description
        }


# class AdzSpider(scrapy.Spider):
#     name = "adzSpider"
#     allowed_domains = ["adz.lk"]
#     start_urls = ["https://adz.lk/ads/"]

#     custom_settings = {
#         "PLAYWRIGHT_BROWSER_OPTIONS": {
#             "headless": False
#         },
#         "PLAYWRIGHT_ABORT_REQUEST": should_abort_request,
#         "FEEDS": {
#                     "%(name)s_%(time)s.json": {
#                         "format": "json",
#                         "overwrite": True,

#                         }
#                 }
#     }

#     def start_requests(self):
#         url = self.start_urls[0]
#         yield scrapy.Request(
#             url,
#             meta={
#                 "playwright": True,
#                 "playwright_include_page": True,
#                 "playwright_page_methods": [
#                     PageMethod("wait_for_selector", ".listivo-listing-grid a")
#                 ],
#                 "errback": self.errback
#             }
#         )

#     async def parse(self, response):
#         # Get the Playwright page instance
#         page = response.meta["playwright_page"]

#         # Get all ad links on the current page
#         # ad_links = response.css(".listivo-listing-grid a::attr(href)").getall()

#         ad_links_elements = await page.query_selector_all(".listivo-listing-grid a")
#         ad_links = [await element.get_attribute('href') for element in ad_links_elements]

#         self.logger.info(response.url)

#         for ad_link in ad_links:
#             yield response.follow(
#                 ad_link,
#                 callback = self.parse_ad,
#                 meta={
#                     "playwright": True,
#                     "playwright_include_page": True,
#                     "playwright_page_methods": [
#                         PageMethod("wait_for_selector", ".elementor-column")
#                     ]
#                 }
#             )

#         # Pagination logic
#         next_button = await page.query_selector("div.listivo-search-results__pagination-desktop div.listivo-pagination__item:last-child")

#         is_disabled = re.search(r'--disabled', await next_button.get_attribute('class')) is not None
#         # Check if the next button is disabled
#         if not is_disabled:
            
#             await next_button.click()
#             # new_url = page.url
#             # self.logger.info(new_url)
#             # Close the Playwright page
            
#             new_url = page.url  
#             yield scrapy.Request(new_url, callback=self.parse,
#                                  meta={
#                                      "playwright": True,
#                                      "playwright_include_page": True,
#                                      "playwright_page_methods": [
#                                          PageMethod(
#                                              "wait_for_selector", ".listivo-listing-grid a")
#                                      ]
#                                  })

#         await page.close()  # Close the page after scraping

           

#     async def parse_ad(self, response):
#         # Get the Playwright page instance for the ad page and close it
#         page = response.meta.get("playwright_page")
#         if page:
#             await page.close()  # Close the ad page after scraping
#         # Scrape ad details from each individual ad page
#         yield {
#             "url": response.url,
#             "title": response.css("h1.listivo-listing-name::text").get(),
#         }

       

#     async def errback(self, failure):
#         page = failure.request.meta["playwright_page"]
#         await page.close()


# class AdzSpider(scrapy.Spider):
#     name = "adzSpider"
#     allowed_domains = ["adz.lk"]
#     start_urls = ["https://adz.lk/ads/"]

#     custom_settings = {
#         "PLAYWRIGHT_BROWSER_OPTIONS": {
#             "headless": False
#         },
#         # This should be a function, not a string
#         "PLAYWRIGHT_ABORT_REQUEST": should_abort_request,
#         "FEEDS": {
#             "%(name)s_%(time)s.json": {
#                 "format": "json",
#                 "overwrite": True,
#             }
#         }
#     }

#     def start_requests(self):
#         url = self.start_urls[0]
#         yield scrapy.Request(
#             url,
#             meta={
#                 "playwright": True,
#                 "playwright_include_page": True,
#                 "playwright_page_methods": [
#                     PageMethod("wait_for_selector", ".listivo-listing-grid a")
#                 ],
#                 "errback": self.errback
#             }
#         )

#     async def parse(self, response):
#         page = response.meta["playwright_page"]

#         ad_links_elements = await page.query_selector_all(".listivo-listing-grid a")
#         ad_links = [await element.get_attribute('href') for element in ad_links_elements]

#         self.logger.info(response.url)

#         for ad_link in ad_links:
#             yield response.follow(
#                 ad_link,
#                 callback=self.parse_ad,
#                 meta={
#                     "playwright": True,
#                     "playwright_include_page": True,
#                     "playwright_page_methods": [
#                         PageMethod("wait_for_selector", ".elementor-column")
#                     ]
#                 }
#             )

#         next_button = await page.query_selector("div.listivo-search-results__pagination-desktop div.listivo-pagination__item:last-child")

#         if next_button:
#             is_disabled = '--disabled' in (await next_button.get_attribute('class') or '')
#             if not is_disabled:
#                 await next_button.click()
#                 new_url = page.url
#                 yield scrapy.Request(
#                     new_url,
#                     callback=self.parse,
#                     meta={
#                         "playwright": True,
#                         "playwright_include_page": True,
#                         "playwright_page_methods": [
#                             PageMethod("wait_for_selector",
#                                        ".listivo-listing-grid a")
#                         ]
#                     }
#                 )

#         await page.close()

#     async def parse_ad(self, response):
#         page = response.meta.get("playwright_page")
#         if page:
#             await page.close()

#         yield {
#             "url": response.url,
#             "title": response.css("h1.listivo-listing-name::text").get(),
#         }

#     async def errback(self, failure):
#         page = failure.request.meta["playwright_page"]
#         await page.close()





        




