import scrapy


class HitadSpider(scrapy.Spider):
    name = "hitad_spider"
    allowed_domains = ["hitad.lk"]
    start_urls = ['https://www.hitad.lk/en/ads']

    def parse(self, response):
        # get all ad links in a page
        ad_links = response.css(".single-ads-product a::attr(href)").getall()

        # follow each ad link and parse the ad
        for ad_link in ad_links:
            yield response.follow(ad_link, self.parse_ad)

        # get the next page link
        # the next page link is in the last li element with an i element
        li_element_with_next_page_link = response.xpath('//ul[@class="pagination justify-content-center"]/li[count(.//i)=1]')
        next_page_link = li_element_with_next_page_link.css('a::attr(href)').get()

        # follow the next page link and parse the ads
        if next_page_link:
            yield response.follow(next_page_link, self.parse)
        

    def parse_ad(self, response):
        # get the url of the ad
        ad_url = response.url
        # get the image urls
        images_urls = response.css("ul#image-gallery li img ::attr(src)").getall()
        # get the ad title
        ad_title = response.css("h1.single-title ::text").get()
        # get the ad details
        more_details = response.css("div.more ul li ::text").getall()
        # get the features
        features = response.css("div.card-body .row .more").css("::text").getall()

        cleaned_features = [item.strip() for item in features if item.strip()]
        # get the breadcrumbs
        breadcrumbs = response.css("ol.breadcrumb li a::text").getall()
        cleaned_breadcrumbs = [item.strip() for item in breadcrumbs if item.strip()]

        desription = []
        date_time = ""
        # get the card body with the ad content        
        haha_row_divs = response.css("div.row.haha div")
        if haha_row_divs:
            temp_description = haha_row_divs[0].css("p ::text").getall()
            # remove empty strings
            desription = [item.strip() for item in temp_description if item.strip()]
            # get the date and time of the ad 
            date_time = desription[-1]
            
        # in some ads the description is in a div with class media
        media_divs = response.css("div.media")
        if media_divs:
            media_divs = media_divs[:-1]
            temp_description = media_divs.css("p ::text").getall()
            # remove empty strings
            desription = [item.strip() for item in temp_description if item.strip()]


        ad   

        yield{
            
            "ad_title": ad_title,
            "more_details": more_details,
            "description": desription,
            "features": cleaned_features,
            "breadcrumbs": cleaned_breadcrumbs,
            "date_time": date_time,
            "ad_url": ad_url,
            "images_urls": images_urls,
            
        }


    
