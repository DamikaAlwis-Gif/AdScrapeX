import scrapy


class HitadSpider(scrapy.Spider):
    name = "hitad_spider"
    allowed_domains = ["hitad.lk"]
    start_urls = ['https://www.hitad.lk/en/ads']

    def parse(self, response):
        ad_links = response.css(".single-ads-product a::attr(href)").getall()
        for ad_link in ad_links:
            yield response.follow(ad_link, self.parse_ad)

        li_element_with_next_page_link = response.xpath('//ul[@class="pagination justify-content-center"]/li[count(.//i)=1]')
        next_page_link = li_element_with_next_page_link.css('a::attr(href)').get()
        if next_page_link:
            yield response.follow(next_page_link, self.parse)
        

    def parse_ad(self, response):
        ad_url = response.url
        images_urls = response.css("ul#image-gallery li img ::attr(src)").getall()
        ad_title = response.css("h1.single-title ::text").get()
        details = response.css("div.more ul li ::text").getall()
        features = response.css("div.card-body .row .more").css("::text").getall()
        # get the card body with the ad content
        haha_row = response.css("div.row.haha")
        if haha_row:
            temp_description = haha_row[0].css("p ::text").getall()
            cleaned_desription = " ".join(
                [item.strip() for item in temp_description if item.strip()])
            date_time = cleaned_desription[-1]

        else:
            cleaned_desription = ""
            date_time = ""
               
       
        
        
        
        yield{
            
            "ad_title": ad_title,
            "details": details,
            "description": cleaned_desription,
            "features": features,
            "date_time": date_time,
            "ad_url": ad_url,
            "images_urls": images_urls,
            
        }


    
