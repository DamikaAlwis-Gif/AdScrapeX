# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from ad_scraper.utils.cleaning import create_combined_description, process_attributes, process_description, set_categories
from itemadapter import ItemAdapter

class AdScraperPipeline:
    def process_item(self, item, spider):
        """Process each scraped item."""
        
        # Create combined description
        item['combined_text'] = create_combined_description(item)

        # Set categories based on breadcrumbs
        set_categories(item)

        # Return the cleaned item
        return item


class HitadAdScraperPipeline:
    def process_item(self, item, spider):
        """Process items for Hitad ads."""
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()

        # Additional processing specific to Hitad ads (if any) can go here
        # Example: Custom field processing or transformations based on field names
        
        # For now, we'll just return the item as is
        return item
