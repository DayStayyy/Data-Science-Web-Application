import argparse
import json
from flask import Flask, render_template, redirect, url_for, request, jsonify, session, make_response,send_file
import pandas as pd
from dataEngine import DataEngine

#python -m flask run --host=0.0.0.0

# we call the file with python3 demo.py --data=DATA_PATH
# get the data path
# parser = argparse.ArgumentParser()
# parser.add_argument('--data', type=str, default='data.csv')
# args = parser.parse_args()
# data_path = args.data
data_path = 'data.csv'

app = Flask(__name__)
if __name__ == '__main__':
    app.run(debug=True)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'


engine = DataEngine(data_path)

@app.route('/api/best_selling_products', methods=['GET', 'POST'])
def best_selling_products():
    # Get the number of products to return
    number = request.args.get('number', default=10, type=int)
    # Get the best selling products
    products = engine.find_best_selling_products(number)
    # Return the results as a json object
    return json.dumps(products.to_dict())


@app.route('/api/most_returned_products', methods=['GET', 'POST'])
def most_returned_products():
    # Get the number of products to return
    number = request.args.get('number', default=10, type=int)
    # Get the most returned products
    products = engine.find_most_returned_products(number)
    # transform the results into a json array
    return json.dumps(products.to_dict())


@app.route('/api/best_customers', methods=['GET', 'POST'])
def best_customers():
    print("YO")
    # Get the number of customers to return
    number = request.args.get('number', default=10, type=int)
    # Get the best customers
    customers = engine.find_best_customers(number)
    # Return the results as a json object
    return json.dumps(customers.to_dict())


@app.route('/api/most_returned_customers', methods=['GET', 'POST'])
def most_returned_customers():
    # Get the number of customers to return
    number = request.args.get('number', default=10, type=int)
    # Get the best customers
    customers = engine.find_most_returned_customers(number)
    # Return the results as a json object
    return json.dumps(customers.to_dict())


@app.route('/api/best_selling_products_by_country', methods=['GET', 'POST'])
def best_selling_products_by_country():
    # Get the number of customers to return
    number = request.args.get('number', default=10, type=int)
    # Get the best customers
    products = engine.find_best_selling_products_by_country(number)
    # Return the results as a json object
    return json.dumps(products)


@app.route('/api/similar_products_countries', methods=['GET', 'POST'])
def similar_products_countries():
    # Get the number of customers to return
    number = request.args.get('number', default=10, type=int)
    # Get the best customers
    products = engine.find_similar_products_countries(number)
    # Return the results as a json object
    return json.dumps(products)


# call find_product_with_biggest_variation
@app.route('/api/product_with_biggest_variation', methods=['GET', 'POST'])
def product_with_biggest_variation():
    # Get the number of customers to return
    number = request.args.get('number', default=10, type=int)
    # other parameters is ascending, start_date, end_date, start_date2, end_date2
    ascending = request.args.get('ascending', default=True, type=int)
    ascending = bool(ascending)
    start_date = request.args.get('start_date', default='2010-12-01', type=str)
    end_date = request.args.get('end_date', default='2011-12-09', type=str)
    start_date2 = request.args.get('start_date2', default='2011-12-01', type=str)
    end_date2 = request.args.get('end_date2', default='2011-12-09', type=str)
    pourcentage = request.args.get('pourcentage', default=0, type=int)
    pourcentage = bool(pourcentage)
    type = request.args.get('type', default='Description', type=str)

    # Get the best customers
    products = engine.find_product_customer_with_biggest_variation(start_date, end_date, start_date2, end_date2, number=number, ascending=ascending, type=type, pourcentage=pourcentage)
    # Return the results as a json object
    return json.dumps(products)


# Modelisation
@app.route('/modelisation/plot_top_product', methods=['GET', 'POST'])
def plot_top_product():
    # Get the number of customers to return
    id = request.args.get('id', default=0, type=int)
    # The fonction create a image in the folder modelisation, the id is the name of the image
    engine.plot_top_product(id)
    filename = 'modelisation/' + str(id) + '.png'

    # Return the image
    return send_file(filename, mimetype='image/gif')

@app.route('/modelisation/plot_top_returned_customers', methods=['GET', 'POST'])
def plot_top_returned_customers():
    # Get the number of customers to return
    id = request.args.get('id', default=0, type=int)
    # The fonction create a image in the folder modelisation, the id is the name of the image
    engine.plot_top_returned_customers(id)
    filename = 'modelisation/' + str(id) + '.png'

    # Return the image
    return send_file(filename, mimetype='image/gif')


@app.route('/modelisation/plot_customer_purchases_in_period', methods=['GET', 'POST'])
def plot_customer_purchases_in_period():
    # Get the number of customers to return
    id = request.args.get('id', default=0, type=int)
    # The fonction create a image in the folder modelisation, the id is the name of the image
    engine.plot_customer_purchases_in_period( id)
    filename = 'modelisation/' + str(id) + '.png'

    # Return the image
    return send_file(filename, mimetype='image/gif')

@app.route('/modelisation/plot_top_products_by_country', methods=['GET', 'POST'])
def plot_top_products_by_country():
    # Get the number of customers to return
    id = request.args.get('id', default=0, type=int)
    # The fonction create a image in the folder modelisation, the id is the name of the image
    engine.plot_top_products_by_country( id)
    filename = 'modelisation/' + str(id) + '.png'

    # Return the image
    return send_file(filename, mimetype='image/gif')

@app.route('/modelisation/plot_top_customers', methods=['GET', 'POST'])
def plot_top_customers():
    # Get the number of customers to return
    id = request.args.get('id', default=0, type=int)
    # The fonction create a image in the folder modelisation, the id is the name of the image
    engine.plot_top_customers(id)
    filename = 'modelisation/' + str(id) + '.png'

    # Return the image
    return send_file(filename, mimetype='image/gif')

@app.route('/modelisation/plot_top_returned_products', methods=['GET', 'POST'])
def plot_top_returned_products():
    # Get the number of customers to return
    id = request.args.get('id', default=0, type=int)
    # The fonction create a image in the folder modelisation, the id is the name of the image
    engine.plot_top_returned_products( id)
    filename = 'modelisation/' + str(id) + '.png'

    # Return the image
    return send_file(filename, mimetype='image/gif')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
