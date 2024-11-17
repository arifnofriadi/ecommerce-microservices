from flask import Flask, jsonify, request
from pymongo import MongoClient
from urllib.parse import quote_plus
from bson import ObjectId
import requests
import os

app = Flask(__name__)

# set up mongodb connection
username = os.getenv("MONGO_USER", "root")  
password = os.getenv("MONGO_PASSWORD", "Dev@root23")

# encoding username and password
encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

# determine mongo uri basen on environment
mongo_host = os.getenv("MONGO_HOST", "localhost" if os.getenv("HOSTNAME") is None else "review-db")
mongo_port = os.getenv("MONGO_PORT", "27017")
mongo_db = os.getenv("MONGO_DB", "review_service")
mongo_auth_source = os.getenv("MONGO_AUTH_SOURCE", "admin")

MONGO_URI = f"mongodb://{encoded_username}:{encoded_password}@{mongo_host}:{mongo_port}/{mongo_db}?authSource={mongo_auth_source}"

# connect to mongodb
client = MongoClient(MONGO_URI)
db = client["review_service"]
reviews_collection = db["reviews"]

# determineproduct service url base on environment
product_service_host = "localhost" if os.getenv("HOSTNAME") is None else "product-service"
PRODUCT_SERVICE_URL = f"http://{product_service_host}:3000/products/"

# Helper to get product data from product service
def get_product_data(product_id):
    try:
        response = requests.get(f'{PRODUCT_SERVICE_URL}{product_id}')
        print(f"Requesting: {PRODUCT_SERVICE_URL}{product_id}")
        if response.status_code == 200:
            return response.json().get("data")
        else:
            print(f"Error fetching product: {response.status_code} - {response.text}")  # Log error
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching product data: {e}")
        return None

# Helper to format MongoDB ObjectId as string
def format_review_id(review):
    review["_id"] = str(review["_id"])
    return review

# Get all reviews
@app.route('/reviews', methods=['GET'])
def get_reviews():
    try:
        reviews = [format_review_id(review) for review in reviews_collection.find()]
        result = []
        for review in reviews:
            product_data = get_product_data(review["product_id"])
            if product_data:
                result.append({
                    "id": review["_id"],
                    "product_id": review["product_id"],
                    "review": review["review"],
                    "product": product_data
                })
        
        return jsonify({
            "message": "All reviews fetched successfully",
            "data": result
        }), 200
    
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Error fetching reviews"
        }), 500
    

# Get reviews by product id
@app.route("/products/<int:product_id>/reviews", methods=["GET"])
def get_reviews_by_product(product_id):
    try:
        product_data = get_product_data(product_id)
        if not product_data:
            return jsonify({"message": "Product not found"}), 404

        reviews = [format_review_id(review) for review in reviews_collection.find({"product_id": product_id})]

        response = {
            "product_id": product_id,
            "product": product_data,
            "reviews": reviews
        }

        return jsonify({
            "message": "Reviews fetched successfully",
            "data": response
        }), 200
    
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Error fetching reviews by product"
        }), 500

# Create review
@app.route('/reviews', methods=['POST'])
def create_review():
    try:
        data = request.json
        product_id = data.get("product_id")
        ratings = data.get("ratings")
        comment = data.get("comment")

        if not product_id or not ratings or not comment:
            return jsonify({"message": "Missing product_id, ratings, or comment"}), 400

        product_data = get_product_data(product_id)
        if not product_data:
            return jsonify({"message": "Product not found"}), 404

        review = {
            "product_id": product_id,
            "review": {
                "ratings": ratings,
                "comment": comment
            }
        }

        result = reviews_collection.insert_one(review)

        response = {
            "id": str(result.inserted_id),
            "product_id": product_id,
            "review": review["review"],
            "product": product_data
        }

        return jsonify({
            "message": "Review created successfully",
            "data": response
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Error creating review"
        }), 500

# Delete review
@app.route("/reviews/<string:review_id>", methods=["DELETE"])
def delete_review(review_id):
    try:
        result = reviews_collection.delete_one({"_id": ObjectId(review_id)})
        if result.deleted_count == 0:
            return jsonify({"message": "Review not found"}), 404
        return jsonify({"message": "Review deleted"}), 200
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Error deleting review"
        }), 500


if __name__ == '__main__':
    app.run(debug=True, port=3004, host="0.0.0.0")
