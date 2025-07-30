# utils.py - Minimal placeholder for notebook import

def find_category_and_product_only(user_input, products):
    """
    Returns a string representation of a list of (category, product) tuples
    for products mentioned in user_input.
    """
    import re
    result = []
    user_input_lower = user_input.lower()
    for category, items in products.items():
        for product in items:
            if product.lower() in user_input_lower:
                result.append((category, product))
    return str(result)

def get_products_and_category():
    return {
        'Computers and Laptops': [
            'TechPro Ultrabook',
            'BlueWave Gaming Laptop',
            'PowerLite Convertible',
            'TechPro Desktop',
            'BlueWave Chromebook'
        ],
        'Smartphones and Accessories': [
            'SmartX ProPhone',
            'MobiTech PowerCase',
            'SmartX MiniPhone',
            'MobiTech Wireless Charger',
            'SmartX EarBuds'
        ],
        'Televisions and Home Theater Systems': [
            'CineView 4K TV',
            'SoundMax Home Theater',
            'CineView 8K TV',
            'SoundMax Soundbar',
            'CineView OLED TV'
        ],
        'Gaming Consoles and Accessories': [
            'GameSphere X',
            'ProGamer Controller',
            'GameSphere Y',
            'ProGamer Racing Wheel',
            'GameSphere VR Headset'
        ],
        'Audio Equipment': [
            'AudioPhonic Noise-Canceling Headphones',
            'WaveSound Bluetooth Speaker',
            'AudioPhonic True Wireless Earbuds',
            'WaveSound Soundbar',
            'AudioPhonic Turntable'
        ],
        'Cameras and Camcorders': [
            'FotoSnap DSLR Camera',
            'ActionCam 4K',
            'FotoSnap Mirrorless Camera',
            'ZoomMaster Camcorder',
            'FotoSnap Instant Camera'
        ]
    }

def read_string_to_list(s):
    """
    Converts a string representation of a list of tuples to a Python list.
    Example: "[('Cameras and Camcorders', 'FotoSnap DSLR Camera')]" -> [('Cameras and Camcorders', 'FotoSnap DSLR Camera')]
    """
    import ast
    try:
        result = ast.literal_eval(s)
        if isinstance(result, list):
            return result
        return []
    except Exception:
        return []

def generate_output_string(product_list):
    """
    Given a list of (category, product) tuples, returns a formatted string with product info.
    """
    if not product_list:
        return "No product information available."
    lines = []
    for category, product in product_list:
        lines.append(f"Category: {category}\nProduct: {product}\n")
    return "\n".join(lines)
