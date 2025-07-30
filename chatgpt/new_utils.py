import re
import json

# Sample product catalog for demonstration purposes
PRODUCT_CATALOG = {
    "phone": [
        {
            "name": "smartx pro",
            "description": (
                "The SmartX Pro features a 6.7-inch AMOLED display, 120Hz refresh rate, "
                "and a 50MP triple-camera system for stunning photos."
            ),
            "specs": {
                "display": "6.7-inch AMOLED",
                "refresh_rate": "120Hz",
                "camera": "50MP triple-camera",
                "battery": "5000mAh",
                "processor": "Octa-core 3.0GHz",
            },
            "price": "$999"
        }
    ],
    "camera": [
        {
            "name": "fotosnap dslr",
            "description": (
                "The FotoSnap DSLR offers a 24.2MP CMOS sensor, full HD 60fps video recording, "
                "and compatibility with a wide range of interchangeable lenses."
            ),
            "specs": {
                "sensor": "24.2MP CMOS",
                "video": "1080p@60fps",
                "iso_range": "100-25600",
                "lens_mount": "EF-Mount",
            },
            "price": "$799"
        }
    ],
    "tv": [
        {
            "name": "visionmax 55 inch",
            "description": (
                "VisionMax 55\" 4K UHD Smart TV with HDR10+ support, integrated voice assistant, "
                "and seamless streaming capabilities."
            ),
            "specs": {
                "size": "55-inch",
                "resolution": "4K UHD",
                "hdr": "HDR10+",
                "smart_os": "VisionOS",
            },
            "price": "$599"
        },
        {
            "name": "visionmax 65 inch",
            "description": (
                "VisionMax 65\" 4K UHD Smart TV with HDR10+ support, integrated voice assistant, "
                "and seamless streaming capabilities."
            ),
            "specs": {
                "size": "65-inch",
                "resolution": "4K UHD",
                "hdr": "HDR10+",
                "smart_os": "VisionOS",
            },
            "price": "$799"
        },
        {
            "name": "soundbar x200",
            "description": (
                "X200 Soundbar with Dolby Atmos support, wireless subwoofer, HDMI ARC, "
                "and Bluetooth connectivity for immersive audio."
            ),
            "specs": {
                "channels": "3.1",
                "wireless_subwoofer": "Yes",
                "connectivity": "HDMI ARC, Bluetooth",
            },
            "price": "$299"
        }
    ]
}

def get_products_from_query(message: str) -> str:
    """
    Parses the customer message to find mentioned product categories and specific product names.
    Returns a JSON string representing a list of [category, product_name] pairs.
    If the category is mentioned but no specific product is found, the product_name will be an empty string.
    """
    msg_lower = message.lower()
    results = []

    for category, products in PRODUCT_CATALOG.items():
        matched_names = []
        # Check for explicit product name mentions
        for prod in products:
            if prod['name'].lower() in msg_lower:
                matched_names.append(prod['name'])
        if matched_names:
            for name in matched_names:
                results.append([category, name])
        else:
            # If the category keyword is present but no specific product matched
            if re.search(rf"\b{re.escape(category)}s?\b", msg_lower):
                results.append([category, ""])

    return json.dumps(results)


def read_string_to_list(json_str: str) -> list:
    """
    Converts a JSON string of [category, product_name] pairs into a Python list.
    """
    try:
        data = json.loads(json_str)
        # Validate structure
        if isinstance(data, list) and all(isinstance(item, list) and len(item) == 2 for item in data):
            return data
    except json.JSONDecodeError:
        pass
    raise ValueError("Invalid format for category-product list string")


def get_mentioned_product_info(category_and_product_list: list) -> dict:
    """
    Given a list of [category, product_name] pairs, returns a dict mapping each category
    to a list of product info dicts. If product_name is empty, returns all products in that category.
    """
    info = {}
    for category, name in category_and_product_list:
        catalog_entries = PRODUCT_CATALOG.get(category, [])
        if not catalog_entries:
            continue
        if not name:
            # Return all products for the category
            info[category] = catalog_entries
        else:
            # Find the specific product by exact name match
            for entry in catalog_entries:
                if entry['name'].lower() == name.lower():
                    info.setdefault(category, []).append(entry)
                    break
    return info


def answer_user_msg(user_msg: str, product_info: dict) -> str:
    """
    Constructs a natural language response summarizing the requested product information.
    """
    response_parts = []

    for category, products in product_info.items():
        pretty_cat = category.capitalize()
        if not products:
            continue
        # Intro line per category
        if len(products) > 1:
            response_parts.append(f"Here are the {pretty_cat} products we have:")
        else:
            response_parts.append(f"Information on {pretty_cat}:")

        # Detailed info per product
        for prod in products:
            name = prod['name'].title()
            response_parts.append(f"\n**{name}**")
            response_parts.append(prod['description'])
            specs = ", ".join(f"{k.replace('_', ' ').title()}: {v}" for k, v in prod['specs'].items())
            response_parts.append(f"Specifications: {specs}")
            response_parts.append(f"Price: {prod['price']}\n")

    if not response_parts:
        return "Sorry, I couldn't find any products matching your request."

    return "\n".join(response_parts)
