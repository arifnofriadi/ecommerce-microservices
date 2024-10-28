from flask import Flask, jsonify

app = Flask(__name__)

product_reviews = [
    {
        "id": 1,
        "product_id": 1,
        "review": "Great product"
    },
    {
        "id": 2,
        "product_id": 1,
        "review": "Pretty good"
    },
    {
        "id": 3,
        "product_id": 1,
        "review": "Pretty bad"
    },
    {
        "id": 4,
        "product_id": 2,
        "review": "Good product"
    },
]

@app.route('/reviews', methods=['GET'])
def get_reviews():
    return jsonify(product_reviews)

@app.route('/products/<int:product_id>/reviews', methods=['GET'])
def get_product_reviews(product_id):
    filtered_reviews = [review for review in product_reviews if review['product_id'] == product_id]
    
    if filtered_reviews:
        return jsonify(filtered_reviews)
    else:
        return jsonify({
            "message": "Product not found",
        }), 404

if __name__ == '__main__':
    app.run(debug=True, port=3003, host="0.0.0.0")