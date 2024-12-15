from flask import Flask, render_template, request, jsonify, redirect
from flask_cors import CORS
from modules import functions
from flask_mysqldb import MySQL  # Adding MySQL library

import sys
import os
import pymysql
pymysql.install_as_MySQLdb()

#adds project root to system path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# --------- Flask & CORS ---------
app = Flask(__name__)
CORS(app)

mysql = MySQL(app)

# === Main & Admin Pages ===

@app.route('/', methods=['GET'])
def index():
    return functions.pull_products(mysql)

@app.route('/admin/')
def admin_panel():
    return render_template('admin_panel.html')

@app.route('/add_product', methods=['POST'])
def add_new_product():
    data = request.json
    p_name = data.get("new_p_name")
    p_price = data.get("new_p_price")
    p_stock = data.get("new_p_stock")
    p_cat = data.get("new_p_cat")

    try:
        success, message = functions.add_new_product(p_name, p_price, p_stock, p_cat)

        if success:
            return jsonify({"success": True, "message": "Product added successfully"}), 200
        else:
            return jsonify({"success": False, "message": message}), 500

    except Exception as e:
        print(f"Error adding product: {e}")
        return jsonify({"success": False, "message": "An error occurred while adding the product."}), 500

@app.route('/change_name', methods=['POST'])
def change_p_name():
    data = request.json
    p_id = data.get("product_id")
    new_name = data.get("new_name")
    return functions.product_name_change(p_id , new_name)

@app.route('/admin/update', methods=['POST'])
def update_product():
    try:    # Get the data from the request
        data = request.json
        p_id = data.get("product_id")  # Product ID
        new_name = data.get("new_name")  # New name for the product
        new_price = data.get("new_price")  # New price
        new_stock = data.get("new_stock")  # New stock quantity

        # Call the function to update the product
        

        # Return the response
        return functions.update_product(p_id, new_name, new_price, new_stock)
    except Exception as e:
            print(f"Error in /admin/update route: {e}")
            return jsonify({"success": False, "message": "Failed to update product."}), 500

@app.route('/change_price', methods=['POST'])
def change_price():
    data = request.json
    p_id = data.get("product_id")
    new_price = data.get("new_price")
    return functions.price_manip(p_id , new_price)

@app.route('/less_stock', methods=['POST'])
def remove_x_stock():
    data = request.json
    p_id = data.get("product_id")
    new_stock = data.get("new_stock_less")
    return functions.remove_x_from_product_stock(p_id , new_stock)

@app.route('/more_stock', methods=['POST'])
def add_x_stock():
    data = request.json
    p_id = data.get('p_id')
    new_stock = data.get("new_stock_more")
    return functions.add_x_to_product_stock(new_stock , p_id)

# === User Login Pages & Methods ===
@app.route('/login/', methods=['POST'])
def login():
    data = request.json
    return functions.authenticate_user(data)

@app.route('/logout/')
def logout():
    return redirect('/')

# == Cart Routes ==

@app.route('/cart/save', methods=['POST'])
def save_cart():
    data = request.json
    user_id = data.get("user_id")
    cart_items = data.get("cart_items", [])
    if not user_id or not isinstance(cart_items, list):
        return jsonify({"success": False, "message": "Invalid data format"}), 400
    return functions.save_cart(user_id, cart_items)

# === Get Cart Route ===
@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    return functions.get_cart(user_id)

@app.route('/checkout', methods=['POST'])
def checkout_route():
    data = request.json
    user_id = data.get('user_id')
    cart_items = data.get('cart_items')

    # Call checkout function from functions.py
    response = functions.checkout(user_id, cart_items)
    return response

@app.route('/easteregg' , methods=['GET'])
def easteregg():
    return """⠀⠀⠀⠀⢠⣤⣴⡦⣀⠀⠀⠀⠀
⠀⠀⠀⢠⣿⠡⠀⠀⠙⣆⠀⠀⠀
⠀⠀⣼⡟⠍⠀⠂⠀⡷⣄⣻⡀⠀
⠀⣴⡿⠩⠀⠀⠠⠀⢳⡽⠈⡷⠀
⠀⣯⢣⠇⠀⠀⠀⠀⠀⢰⣆⠨⡇
⠀⣿⣿⡆⠀⠅⠀⠱⠀⠀⠉⠀⡇
⢾⡟⡯⠅⡀⠀⠀⠀⠀⠀⠀⢾⡅
⢸⡿⣿⢥⠌⠱⡘⠢⠠⠀⠀⢾⡅
⠀⠹⣯⣷⡿⣷⣎⠒⢂⣀⣼⠃⠀
⠀⠀⠀⠉⠛⠛⠛⠋⠋⠁⠀⠀⠀
"""

# ======================= DEBUG ==========================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)