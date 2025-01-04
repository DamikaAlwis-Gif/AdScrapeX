# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from ad_scraper.utils.cleaning import create_combined_description, process_attributes, process_description, set_categories
from ad_scraper.utils.transformers import transform_riyasewana_data, transform_ikman_data
from itemadapter import ItemAdapter
from ad_scraper.db_config import create_session
from ad_scraper.models import RawListing
from sqlalchemy.exc import SQLAlchemyError

class SpiderSpecificPipeline:
    """
    Pipeline for transforming spider-specific raw data into a common schema.
    """
    def process_item(self, item, spider):
        # Apply transformations based on spider name
        if spider.name == "riyasewana":
            return transform_riyasewana_data(item)
        elif spider.name == "ikman":
            return transform_ikman_data(item)
        elif spider.name == "hitad":
            # Additional processing for Hitad (if needed)
            return item
        else:
            # Return unmodified item for unknown spiders
            return item

class AdScraperPipeline:
    def __init__(self):
        # Initialize the database session
        self.session = create_session()

    def process_item(self, item, spider):
        """Process each scraped item."""
        
        # Create combined description
        item['combined_text'] = create_combined_description(item)

        # Set categories based on breadcrumbs
        set_categories(item)

        self.save_to_db(item)

        # Return the cleaned item
        return item

    def save_to_db(self, item):
        """Save the item to the PostgreSQL database using SQLAlchemy ORM."""
        try:
            # Create a RawListing instance from the item
            listing = RawListing(
                title=item.get('title'),
                meta_data=item.get('meta_data'),
                price=item.get('price'),
                attributes=item.get('attributes'),
                description=item.get('description'),
                url=item.get('url'),
                breadcrumbs=item.get('breadcrumbs'),
                image_urls=item.get('image_urls'),
                additional_data=item.get('additional_data'),
                combined_text=item.get('combined_text')  # Include combined_text in the database
            )

            # Add the item to the session
            self.session.add(listing)
            self.session.commit()
            print(f"Successfully saved item: {item.get('title')}")

        except SQLAlchemyError as e:
            # Rollback in case of an error and log the exception
            self.session.rollback()
            print(f"Error inserting item into database: {e}")
            

    def close_spider(self, spider):
        """Close the session when the spider finishes."""
        self.session.close()
    

class HitadAdScraperPipeline:
    def process_item(self, item, spider):
        """Process items for Hitad ads."""
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()

        # Additional processing specific to Hitad ads (if any) can go here
        # Example: Custom field processing or transformations based on field names
        
        # For now, we'll just return the item as is
        return item

