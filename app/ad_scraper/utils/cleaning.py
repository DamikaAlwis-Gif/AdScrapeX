import re
import emoji
import logging

def remove_urls(text):
    """Remove URLs from the text."""
    return re.sub(r'http\S+', '', text)

def remove_unnecessary_chars(text):
    """Remove unnecessary characters like emojis and extra spaces."""
    cleaned_text = emoji.replace_emoji(text, replace="")
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    return cleaned_text.strip()

def remove_emoji(text):
    """Remove emojis from the text."""
    return emoji.replace_emoji(text, replace="")

def process_attributes(attributes):
    """Process the attributes to return a cleaned string."""
    attributes_pair = [ f"{key}: {value}" for key, value in attributes.items() ]
    # print("***************************************************")
    # print(attributes)
    # print("***************************************************")

    # if isinstance(attributes, list):
    #     items = attributes  # If attributes is already a list, use it as is
    # else:
    #     items = list(attributes.items())  # Convert the dictionary to a list of key-value pairs
    # i = 0
    # while i < len(attributes) - 1:  # Ensure not going out of bounds
    #     pair = attributes[i] + attributes[i + 1]
    #     i += 2
    #     attributes_pair.append(pair)
    
    # # If there's an odd number of attributes, append the last one
    # if i < len(attributes):
    #     attributes_pair.append(attributes[i])
    
    return ", ".join(attributes_pair)

def process_description(description):
    """Process the description by cleaning unnecessary words and characters."""
    unnecessary_words = ["show more", "Description"]
    pattern = r'\b(?:' + '|'.join(re.escape(word) for word in unnecessary_words) + r')\b'

    if isinstance(description, str):
        description = [description]

    cleaned_description = []
    for item in description:
        item = re.sub(pattern, '', item, flags=re.IGNORECASE)
        item = remove_urls(item)
        item = remove_unnecessary_chars(item)
        cleaned_description.append(item)

    cleaned_description = ". ".join([item.strip() for item in cleaned_description if item.strip()])
    cleaned_description = re.sub(r'\s+', ' ', cleaned_description)
    cleaned_description = re.sub(r'\.\.+', '.', cleaned_description)

    return cleaned_description.strip()

def create_combined_description(row):
    """Create a combined description from title, attributes, and description."""
    title = row["title"]
    attributes = process_attributes(row["attributes"])
    description = process_description(row["description"])
    combined_description = f"{title}. {attributes}. {description}"
    cleaned_description = remove_unnecessary_chars(combined_description)
    return cleaned_description

def set_categories(item):
    """Set category columns based on breadcrumbs."""
    if item is None or len(item) == 0:
        logging.error("Item is None or empty: %s", item)
        return item
    
    # Assuming 'breadcrumbs' is a list within the item
    breadcrumbs = item.get("breadcrumbs", [])
    category_1 = breadcrumbs[2] if len(breadcrumbs) > 2 else ""
    category_2 = breadcrumbs[3] if len(breadcrumbs) > 3 else ""
    category_3 = breadcrumbs[4] if len(breadcrumbs) > 4 else ""

    # Set the category fields directly on the item
    item["category_1"] = category_1
    item["category_2"] = category_2
    item["category_3"] = category_3

    return item
