
"""
common_schema = {
    "title": str,                # Main title of the ad
    "meta_data": str,            # Ad metadata (posted time, location, etc.)
    "price": str,                # Price information
    "attributes": list,          # List of key-value attributes
    "description": str,          # Full description of the ad
    "url": str,                  # URL to the ad
    "breadcrumbs": list,         # Breadcrumb categories
    "image_urls": list,          # List of image URLs
    "additional_data": dict      # Extra spider-specific data (optional)
}
"""


def transform_riyasewana_data(raw_item):
    """
    Transform Riyasewana spider output into the common schema.
    """
    return {
        "title": raw_item.get("ad_title", ""),
        "meta_data": raw_item.get("ad_meta_data", ""),
        "price": extract_field_from_content(raw_item.get("ad_content", []), "Price"),
        "attributes": extract_attributes_from_content(raw_item.get("ad_content", [])),
        "description": combine_description_from_content(raw_item.get("ad_content", [])),
        "url": raw_item.get("ad_url", ""),
        "breadcrumbs": [],  # Riyasewana does not provide breadcrumbs
        "image_urls": [],   # No image URLs in Riyasewana example
        "additional_data": {"raw_content": raw_item.get("ad_content", [])}
    }


def transform_ikman_data(raw_item):
    """
    Transform Ikman spider output into the common schema.
    """
    return {
        "title": raw_item.get("title", ""),
        "meta_data": " ".join(raw_item.get("sub_title", [])),  # Combine subtitle as metadata
        "price": raw_item.get("price", [""])[0],  # Extract first element of the price list
        "attributes": parse_attributes(raw_item.get("attributes", [])),
        "description": combine_description_from_content(raw_item.get("description", [])),
        "url": raw_item.get("url", ""),
        "breadcrumbs": raw_item.get("breadcrumbs", []),
        "image_urls": raw_item.get("image_urls", []),
        "additional_data": {"raw_description": raw_item.get("description", [])}
    }


def extract_field_from_content(content, field_name):
    """
    Extract a specific field (like Price) from ad_content list.
    """
    try:
        index = content.index(field_name)
        return content[index + 1] if index + 1 < len(content) else ""
    except ValueError:
        return ""


def extract_attributes_from_content(content):
    """
    Extract key-value pairs from ad_content as attributes.
    Example: ['Make', 'Toyota', 'Model', 'Camry'] -> {"Make": "Toyota", "Model": "Camry"}
    """
    attributes = {}
    for i in range(0, len(content) - 1, 2):  # Step in pairs
        key = content[i].strip()
        value = content[i + 1].strip()
        if key and value:
            attributes[key] = value
    return attributes


def combine_description_from_content(content):
    """
    Combine description-related fields into a single string.
    """
    return " ".join([line.strip() for line in content if line.strip()])


def parse_attributes(attributes_list):
    """
    Parse Ikman attributes from a list of key-value pairs.
    Example: ['Condition: ', 'New', 'Brand: ', 'MI+'] -> {'Condition': 'New', 'Brand': 'MI+'}
    """
    parsed_attributes = {}
    for i in range(0, len(attributes_list) - 1, 2):  # Step in pairs
        key = attributes_list[i].replace(":", "").strip()
        value = attributes_list[i + 1].strip()
        if key and value:
            parsed_attributes[key] = value
    return parsed_attributes
