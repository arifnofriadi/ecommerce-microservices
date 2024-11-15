from flask import Flask, jsonify, render_template, request
import requests
from functools import lru_cache

app = Flask(__name__)

# get product data
@lru_cache(maxsize=128)
def get_products(product_id):
    try:
        response = requests.get(f'http://localhost:3000/products/{product_id}')
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching product data: {e}")
        return {"error": "Failed to fetch product data"}

# get sold product data
def get_sold_products(product_id):
    try:
        response = requests.get(f'http://localhost:3002/cart/{product_id}')
        response.raise_for_status()
        data = response.json()

        if 'data' in data:
            cart_item = data['data'] 
            total_quantity = 0

            if isinstance(cart_item, dict) and 'product_id' in cart_item:
                if cart_item['product_id'] == product_id:
                    total_quantity = cart_item.get('quantity', 0)

            print(f"Total quantity for product_id {product_id}: {total_quantity}")
            return total_quantity
        else:
            print("Invalid data format:", data)
            return 0  
    except requests.exceptions.RequestException as e:
        print(f"Error fetching sold product data: {e}")
        return {"error": "Failed to fetch sold product data"}

# get review data
def get_reviews(product_id):
    try:
        response = requests.get(f'http://localhost:3004/products/{product_id}/reviews')
        response.raise_for_status()
        data = response.json()

        return data.get('data', {"reviews": [], "product": {}})
    except requests.exceptions.RequestException as e:
        print(f"Error fetching review data: {e}")
        return {"error": "Failed to fetch review data"}

@app.route('/product/<int:product_id>')
def get_product_info(product_id):
    # Retrieve data from each service
    product = get_products(product_id)
    cart = get_sold_products(product_id)
    review = get_reviews(product_id)

    # Merge all data into one object
    combined_response = {
        "product": product if "error" not in product else None,
        "cart": cart, 
        "reviews": review.get("reviews", []) if "error" not in review else []
    }

    #  returning responses in JSON format if the parameter ?format=json is added
    if request.args.get('format') == 'json':
        return jsonify({
            "data": combined_response,
            "message": "Product data fetched successfully" if product else "Failed to fetch product data"
        })

    return render_template('product.html', **combined_response)

if __name__ == '__main__':
    app.run(debug=True, port=3005)
