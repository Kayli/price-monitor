import random
import asyncio

from quart import Quart, jsonify, make_response

app = Quart(__name__)


def generate_fake_product(product_id):
    product_data = {
        "id": product_id,
        "name": f"Product {product_id}",
        "description": f"This is a description for product {product_id}.",
        "price": round(random.uniform(10.0, 100.0), 2),  # Random price between 10.0 and 100.0
        "currency": "USD"
    }
    return product_data


@app.route('/check-ready', methods=['GET'])
async def check_ready():
    response = await make_response("Ready!", 200)
    return response


@app.route('/products/<product_id>', methods=['GET'])
async def get_product(product_id):
    product = generate_fake_product(product_id)
    await asyncio.sleep(random.uniform(0.2, 1.0)) # simulate processing delay
    return jsonify(product)


if __name__ == '__main__':
    # run flask web server listening on all available interfaces
    # known bug: debug=False breaks graceful shutdown via SIGTERM
    app.run(host='0.0.0.0', port=5000, debug=True)
