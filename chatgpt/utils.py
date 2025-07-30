
import openai

products = {
    'Computers and Laptops': [
        {'name': 'TechPro Ultrabook', 'price': 1199},
        {'name': 'BlueWave Gaming Laptop', 'price': 1599},
        {'name': 'PowerLite Convertible', 'price': 999},
        {'name': 'TechPro Desktop', 'price': 799},
        {'name': 'BlueWave Chromebook', 'price': 399}
    ],
    'Smartphones and Accessories': [
        {'name': 'SmartX ProPhone', 'price': 899},
        {'name': 'MobiTech PowerCase', 'price': 59},
        {'name': 'SmartX MiniPhone', 'price': 599},
        {'name': 'MobiTech Wireless Charger', 'price': 39},
        {'name': 'SmartX EarBuds', 'price': 99}
    ],
    'Televisions and Home Theater Systems': [
        {'name': 'CineView 4K TV', 'price': 1099},
        {'name': 'SoundMax Home Theater', 'price': 799},
        {'name': 'CineView 8K TV', 'price': 2099},
        {'name': 'SoundMax Soundbar', 'price': 199},
        {'name': 'CineView OLED TV', 'price': 1799}
    ],
    'Gaming Consoles and Accessories': [
        {'name': 'GameSphere X', 'price': 499},
        {'name': 'ProGamer Controller', 'price': 69},
        {'name': 'GameSphere Y', 'price': 399},
        {'name': 'ProGamer Racing Wheel', 'price': 149},
        {'name': 'GameSphere VR Headset', 'price': 299}
    ],
    'Audio Equipment': [
        {'name': 'AudioPhonic Noise-Canceling Headphones', 'price': 199},
        {'name': 'WaveSound Bluetooth Speaker', 'price': 129},
        {'name': 'AudioPhonic True Wireless Earbuds', 'price': 149},
        {'name': 'WaveSound Soundbar', 'price': 179},
        {'name': 'AudioPhonic Turntable', 'price': 249}
    ],
    'Cameras and Camcorders': [
        {'name': 'FotoSnap DSLR Camera', 'price': 549},
        {'name': 'ActionCam 4K', 'price': 299},
        {'name': 'FotoSnap Mirrorless Camera', 'price': 799},
        {'name': 'ZoomMaster Camcorder', 'price': 449},
        {'name': 'FotoSnap Instant Camera', 'price': 99}
    ]
}

def find_category_and_product_only(user_input, products):
    result = []
    user_input_lower = user_input.lower()
    for category, items in products.items():
        for product in items:
            # product is now a dict
            if product['name'].lower() in user_input_lower:
                result.append((category, product['name'], product['price']))
    return str(result)

def read_string_to_list(s):
    import ast
    try:
        result = ast.literal_eval(s)
        if isinstance(result, list):
            return result
        return []
    except Exception:
        return []

def generate_output_string(product_list):
    if not product_list:
        return "No product information available."
    lines = []
    for item in product_list:
        # item can be (category, product, price) or (category, product)
        if len(item) == 3:
            category, product, price = item
            lines.append(f"Category: {category}\nProduct: {product}\nPrice: ${price}\n")
        else:
            category, product = item
            lines.append(f"Category: {category}\nProduct: {product}\n")
    return "\n".join(lines)

def get_completion_from_messages(messages):
    # Placeholder for actual OpenAI call
    return "[MOCKED] Response based on messages: " + str(messages)

def process_user_message(user_input, all_messages, debug=True):
    delimiter = "```"
    # Step 1: Check input to see if it flags the Moderation API or is a prompt injection
    response = openai.moderations.create(input=user_input)
    moderation_output = response.results[0]
    if moderation_output.flagged:
        print("Step 1: Input flagged by Moderation API.")
        return "Sorry, we cannot process this request."
    if debug: print("Step 1: Input passed moderation check.")
    category_and_product_response = find_category_and_product_only(user_input, products)
    category_and_product_list = read_string_to_list(category_and_product_response)
    if debug: print("Step 2: Extracted list of products.")
    product_information = generate_output_string(category_and_product_list)
    if debug: print("Step 3: Looked up product information.")
    system_message = f"""
    You are a customer service assistant for a large electronic store. \
    Respond in a friendly and helpful tone, with concise answers. \
    Make sure to ask the user relevant follow-up questions.
    """
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': f"{delimiter}{user_input}{delimiter}"},
        {'role': 'assistant', 'content': f"Relevant product information:\n{product_information}"}
    ]
    final_response = get_completion_from_messages(all_messages + messages)
    if debug:print("Step 4: Generated response to user question.")
    all_messages = all_messages + messages[1:]
    # Step 5: Put the answer through the Moderation API
    response = openai.moderations.create(input=final_response)
    moderation_output = response.results[0]
    if moderation_output.flagged:
        if debug: print("Step 5: Response flagged by Moderation API.")
        return "Sorry, we cannot provide this information."
    if debug: print("Step 5: Response passed moderation check.")
    user_message = f"""
    Customer message: {delimiter}{user_input}{delimiter}
    Agent response: {delimiter}{final_response}{delimiter}
    Does the response sufficiently answer the question?
    """
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_message}
    ]
    evaluation_response = get_completion_from_messages(messages)
    if debug: print("Step 6: Model evaluated the response.")
    if "Y" in evaluation_response:
        if debug: print("Step 7: Model approved the response.")
        return final_response, all_messages
    else:
        if debug: print("Step 7: Model disapproved the response.")
        neg_str = "I'm unable to provide the information you're looking for. I'll connect you with a human representative for further assistance."
        return neg_str, all_messages

if __name__ == "__main__":
    user_input = "tell me about the smartx pro phone and the fotosnap camera, the dslr one. Also what tell me about your tvs"
    response,_ = process_user_message(user_input,[])
    print(response)
