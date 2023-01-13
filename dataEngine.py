import pandas as pd
import matplotlib.pyplot as plt



class DataEngine(object):
    def __init__(self, path):
        self.df = pd.read_csv(path, encoding='ISO-8859-1')


    def find_best_selling_products(self, n=10):
        products = self.df.groupby('Description').sum(numeric_only=False)['Quantity']
        products = products.sort_values(ascending=False)
        return products.head(n)

    def find_most_returned_products(self, n=10):
        products = self.df[self.df['Quantity'] < 0].groupby('Description').sum(numeric_only=False)['Quantity']
        products = products.sort_values(ascending=True)
        return products.head(n)

    def find_best_customers(self, n=10):
        customers = self.df.groupby('CustomerID').sum(numeric_only=False)['Quantity']
        customers = customers.sort_values(ascending=False)
        return customers.head(n)

    def find_most_returned_customers(self, n=10):
        customers = self.df[self.df['Quantity'] < 0].groupby('CustomerID').sum(numeric_only=False)['Quantity']
        customers = customers.sort_values(ascending=True)
        return customers.head(n)

    def find_best_selling_products_by_country(self, n=10):
        # Only get rows where quantity is greater than zero (to ignore returns)
        df = self.df[self.df['Quantity'] > 0]
        countries_products = df.groupby(['Country','Description']).sum(numeric_only=False).reset_index()
        countries_products = countries_products.sort_values(by=['Country','Quantity'],ascending=[True,False])
        products_by_country = {}
        for country, df_country in countries_products.groupby('Country'):
            products = df_country.head(n)["Description"].tolist()
            products_by_country[country] = products
        return products_by_country

    def find_similar_products_countries(self, n=10):
        # Create a df with the top n products in the United Kingdom
        df_uk = self.df[self.df['Country'] == 'United Kingdom']
        uk_products = df_uk.groupby('Description').sum(numeric_only=False).nlargest(n, 'Quantity')
        uk_products = uk_products.index.tolist()

        # Group the original df by country and get the top n products for each country
        countries_products = self.df.groupby(['Country','Description']).sum(numeric_only=False).reset_index()
        countries_products = countries_products.sort_values(by=['Country','Quantity'],ascending=[True,False])
        countries_products = countries_products.groupby('Country').head(n)
        similar_countries = {}

        # Iterate over the countries and compare the top n products to the UK products
        for country, df_country in countries_products.groupby('Country'):
            country_products = df_country['Description'].tolist()
            common_products = set(country_products).intersection(uk_products)
            if len(common_products) > 0:
                similar_countries[country] = common_products
        return similar_countries


    # ============= Modelisation ================ #

    def plot_top_returned_products(self):
        # Only get rows where quantity is less than zero
        self.df = self.df[self.df['Quantity'] < 0]
        # Group by product and sum the quantity
        products = self.df.groupby('Description').sum(numeric_only=False)['Quantity']
        # Sort products by quantity, but since it's negative we sort in ascending order
        products = products.sort_values(ascending=True)
        # Plot the top 10 returned products
        ax = products[:10].plot(kind='bar')
        ax.invert_yaxis()
        plt.xlabel('Quantity Returned')
        plt.ylabel('Product')
        plt.title('Top 10 Returned Products')
        return plt