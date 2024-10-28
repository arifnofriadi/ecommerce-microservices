from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

def get_products(product_id):
    try:
        response = requests.get(f'http://localhost:3000/products/{product_id}')
        response.raise_for_status()  # Cek jika ada error HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching product data: {e}")
        return {"error": "Failed to fetch product data"}

def get_sold_products(product_id):
    try:
        response = requests.get(f'http://localhost:3002/carts/{product_id}')
        response.raise_for_status()
        return response.json().get('total_quantity', 0)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching sold product data: {e}")
        return {"error": "Failed to fetch sold product data"}

def get_reviews(product_id):
    try:
        response = requests.get(f'http://localhost:3003/products/{product_id}/reviews')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching review data: {e}")
        return {"error": "Failed to fetch review data"}

@app.route('/product/<int:product_id>')
def get_product_info(product_id):
    # get products
    product = get_products(product_id)

    # get cart
    cart = get_sold_products(product_id)

    # get reviews
    review = get_reviews(product_id)

    # Gabungkan semua data ke dalam satu respons JSON
    # return jsonify({
    #     "product": product,
    #     "cart": cart,
    #     "review": review
    # })

    return render_template('product.html', product=product, cart=cart, review=review)

if __name__ == '__main__':
    app.run(debug=True, port=3004)
