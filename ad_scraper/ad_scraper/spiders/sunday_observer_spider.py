import json
import scrapy


class SundayObserverSpider(scrapy.Spider):
    name = "sunday_observer_spider"
    allowed_domains = ["sundayobserver.lk", "proxy.scrapeops.io"]
    start_urls = ["https://sundayobserver.lk/classifieds/"]
    # settings.py



    def parse(self, response):
        # Select all <a> tags
        a_tags = response.css(".penci-bgitem .cat a")
        
        for a_tag in a_tags:
            url = a_tag.attrib.get("href")
            category = a_tag.css("span::text").get()

            yield response.follow(url, self.parse_category)


    def parse_category(self, response):
       
        ad_links = response.css("li.list-post a.penci-btn-readmore ::attr(href)").getall() 
        for ad_link in ad_links:
            yield response.follow(ad_link, self.parse_ad)

        ajax_url = "https://www.sundayobserver.lk/wp-admin/admin-ajax.php"  

        load_more_button = response.css("div.penci-ajax-more a")
        data_layout = load_more_button.css("::attr(data-layout)").get()
        data_number = load_more_button.css("::attr(data-number)").get()
        data_offset = load_more_button.css("::attr(data-offset)").get()
        data_from = load_more_button.css("::attr(data-from)").get()
        data_template = load_more_button.css("::attr(data-template)").get()
        data_archivetype = load_more_button.css("::attr(data-archivetype)").get()
        data_archivevalue = load_more_button.css("::attr(data-archivevalue)").get()
        data_order = load_more_button.css("::attr(data-order)").get()


        
       
        form_data = {
            'action': 'penci_archive_more_post_ajax',
            'order': data_order,
            'offset': data_offset,
            'layout': data_layout,
            'from': data_from,
            'template': data_template,
            'ppp': data_number,
            'archivetype': data_archivetype,
            'archivevalue': data_archivevalue,           
            'nonce': '4fd3ec5149',
        }

        yield scrapy.FormRequest(
            url= ajax_url,
            formdata=form_data,
            callback=self.parse_category,
        )

   


        
          

    def parse_ad(self, response):
        header = response.css("div.header-standard")
        category = header.css("span.cat a span ::text").get()
        date_time = header.css("div.post-box-meta-single span ::text").get()
        image_url = response.css("div.post-image a ::attr(href)").get()
        inner_post = response.css("div.inner-post-entry")
        title = inner_post.css("p strong ::text").get()
        description = inner_post.css("p ::text").getall()[1]
        yield {
            "category": category,
            "date_time": date_time,
            "image_url": image_url,
            "title": title,
            "description": description,
            "url": response.url
        }

              


           
                

            
