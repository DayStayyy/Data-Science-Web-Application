import json
from flask import Flask, render_template, redirect, url_for, request, jsonify, session, make_response
import pandas as pd
from dataEngine import DataEngine

#python -m flask run --host=0.0.0.0

app = Flask(__name__)
app.run(debug=True)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'


engine = DataEngine('data.csv')


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
    return jsonify(products)

@app.route('/api/similar_products_countries', methods=['GET', 'POST'])
def similar_products_countries():
    # Get the number of customers to return
    number = request.args.get('number', default=10, type=int)
    # Get the best customers
    products = engine.find_similar_products_countries(number)
    # Return the results as a json object
    return jsonify(products)

# call find_product_with_biggest_variation
@app.route('/api/product_with_biggest_variation', methods=['GET', 'POST'])
def product_with_biggest_variation():
    # Get the number of customers to return
    number = request.args.get('number', default=10, type=int)
    # other parameters is ascending, start_date, end_date, start_date2, end_date2
    ascending = request.args.get('ascending', default=True, type=bool)
    start_date = request.args.get('start_date', default='2010-12-01', type=str)
    end_date = request.args.get('end_date', default='2011-12-09', type=str)
    start_date2 = request.args.get('start_date2', default='2011-12-01', type=str)
    end_date2 = request.args.get('end_date2', default='2011-12-09', type=str)
    # Get the best customers
    products = engine.find_product_with_biggest_variation(start_date, end_date, start_date2, end_date2, number=number, ascending=ascending)
    # Return the results as a json object
    return jsonify(products)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
