import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

type = {
    'Description': 1,
    'Quantity': 2,
    'CustomerID': 3,
    'Country': 4
}

class DataEngine(object):
    def __init__(self, path):
        self.df = pd.read_csv(path, encoding='ISO-8859-1')
        self.fill_na_description()
        self.fill_none_description()
        self.clean_dates()
        self.convert_float_to_int()
        self.remove_non_uppercase_description()
        self.reset_index_and_save('to_csv.csv')
        self.df = pd.read_csv('to_csv.csv', encoding='ISO-8859-1')


    # Clean the data
    def fill_na_description(self):
        most_common_description_by_stockcode = self.df.groupby("StockCode")["Description"].first()
        self.df["Description"].fillna(self.df["StockCode"].map(most_common_description_by_stockcode), inplace=True)
        return self.df.head()

    def fill_none_description(self):
        most_common_description_by_stockcode = self.df.groupby("StockCode")["Description"].apply(lambda x:x.value_counts().idxmax() if x.count() else None)
        most_common_description_by_stockcode.fillna('', inplace = True)
        self.df["Description"].fillna(self.df["StockCode"].map(most_common_description_by_stockcode), inplace=True)
        return self.df.head()

    def clean_dates(self):
        # convert "InvoiceDate" column to datetime
        self.df["InvoiceDate"] = pd.to_datetime(self.df["InvoiceDate"])

        # extract date only
        self.df["InvoiceDate"] = self.df["InvoiceDate"].dt.date
        return self.df.head()
        
    def convert_float_to_int(self):
        self.df["CustomerID"] = self.df["CustomerID"].fillna(-1)
        self.df["CustomerID"] = self.df["CustomerID"].astype(int)
        return self.df.head()
    # Remove "?", "damaged", "check", etc.
    def remove_non_uppercase_description(self):
        self.df.drop(self.df[~self.df['Description'].str.isupper()].index, inplace = True)
        return self.df.head()

    def reset_index_and_save(self, file_path):
        self.df.reset_index(drop=True, inplace=True)
        self.df.to_csv(file_path, index=False)


    # Backend functions

    def find_best_selling_products(self, number=10):
        products = self.df.groupby('Description').sum(numeric_only=False)['Quantity']
        products = products.sort_values(ascending=False)
        return products.head(number)

    def find_most_returned_products(self, number=10):
        products = self.df[self.df['Quantity'] < 0].groupby('Description').sum(numeric_only=False)['Quantity']
        products = products.sort_values(ascending=True)
        return products.head(number)


    def find_best_customers(self, number=10):
        customers = self.df.groupby('CustomerID').sum(numeric_only=False)['Quantity']
        customers = customers.sort_values(ascending=False)
        return customers.head(number)

    def find_most_returned_customers(self, number=10):
        customers = self.df[self.df['Quantity'] < 0].groupby('CustomerID').sum(numeric_only=False)['Quantity']
        customers = customers.sort_values(ascending=True)
        return customers.head(number)

    def find_best_selling_products_by_country(self, number=10):
        # Only get rows where quantity is greater than zero (to ignore returns)
        df = self.df[self.df['Quantity'] > 0]
        countries_products = df.groupby(['Country','Description']).sum(numeric_only=False).reset_index()
        countries_products = countries_products.sort_values(by=['Country','Quantity'],ascending=[True,False])
        products_by_country = {}
        for country, df_country in countries_products.groupby('Country'):
            products = df_country.head(number)["Description"].tolist()
            products_by_country[country] = products
        return products_by_country

    def find_similar_products_countries(self, number=10):
        # Create a df with the top number products in the United Kingdom
        df_uk = self.df[self.df['Country'] == 'United Kingdom']
        uk_products = df_uk.groupby('Description').sum(numeric_only=False).nlargest(number, 'Quantity')
        uk_products = uk_products.index.tolist()

        # Group the original df by country and get the top number products for each country
        countries_products = self.df.groupby(['Country','Description']).sum(numeric_only=False).reset_index()
        countries_products = countries_products.sort_values(by=['Country','Quantity'],ascending=[True,False])
        countries_products = countries_products.groupby('Country').head(number)
        similar_countries = {}

        # Iterate over the countries and compare the top number products to the UK products
        for country, df_country in countries_products.groupby('Country'):
            country_products = df_country['Description'].tolist()
            common_products = set(country_products).intersection(uk_products)
            if len(common_products) > 0:
                similar_countries[country] = common_products
        return similar_countries

    def find_product_customer_with_biggest_variation(self, start_date, end_date, start_date2, end_date2, number = 10, ascending = False, type='Description', pourcentage = False):
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)
            start_date2 = pd.to_datetime(start_date2)
            end_date2 = pd.to_datetime(end_date2)
            # Filter the dataframe to only include the products that were sold in the given time period
            df1 = self.df[(pd.to_datetime(self.df['InvoiceDate']) >= start_date) & (pd.to_datetime(self.df['InvoiceDate']) <= end_date)]
            df2 = self.df[(pd.to_datetime(self.df['InvoiceDate']) >= start_date2) & (pd.to_datetime(self.df['InvoiceDate']) <= end_date2)]
            df1 = df1[df1['Quantity'] > 0]
            df2 = df2[df2['Quantity'] > 0]
            df1 = df1.groupby(type)[['Quantity']].sum(numeric_only=False).reset_index()
            df2 = df2.groupby(type)[['Quantity']].sum(numeric_only=False).reset_index()
            # calculate total quantity sold for each product
            df1 = df1.sort_values(by=['Quantity'],ascending=ascending)
            df2 = df2.sort_values(by=['Quantity'],ascending=ascending)
            # calculate the variation between the two time periods for each product in percentage
            df = pd.merge(df1, df2, on=type, how='outer')
            if pourcentage == True:
                df['Variation'] = (df['Quantity_y'] - df['Quantity_x']) / df['Quantity_x'] * 100
            else:
                df['Variation'] = df['Quantity_y'] - df['Quantity_x']
            df = df.sort_values(by=['Variation'],ascending=ascending)
            df = df.dropna()
            # delete the columns that are not needed , Quantity_x and Quantity_y
            df = df.drop(['Quantity_x', 'Quantity_y'], axis=1)
            # sort the dataframe by variation in ascending order
            df = df.sort_values(by=['Variation'],ascending=ascending)
            # return as a dict 
            dict = {}
            for _, row in df.iterrows():
                dict[row[type]] = row['Variation']
                if len(dict) == number:
                    break
            return dict
            

    

    # ============= Modelisation ================ #

    def plot_top_product(self, id):
        # Group the data by product and sum the quantity
        products = self.df.groupby('Description').sum(numeric_only=False)['Quantity']
        # Sort the products by quantity
        products = products.sort_values(ascending=False)
        # Plot the top 10 products
        products.iloc[:10].plot(kind='bar')
        plt.xlabel('Product')
        plt.ylabel('Quantity Sold')
        plt.title('Top 10 Selling Products')
        plt.savefig(f'modelisation/{id}.png', bbox_inches='tight')

    def plot_top_returned_customers(self, id):
        # Group by customer and sum the Quantity
        products = self.df.groupby('CustomerID')['Quantity'].sum(numeric_only=False)
        # Sort customer by quantity, but since it's negative we sort in ascending order
        products = products.sort_values(ascending=True)
        # Plot the top 10 returned customers
        ax = products.iloc[:10].plot(kind='bar')
        ax.invert_yaxis()
        plt.ylabel('Quantity Returned')
        plt.xlabel('Customers')
        plt.title('Top 10 Returned Customers')
        plt.savefig(f'modelisation/{id}.png', bbox_inches='tight')
        
    def plot_top_returned_products(self, id):
        # Only get rows where quantity is less than zero
        dataframe_products = self.df[self.df['Quantity'] < 0]
        # Group by product and sum the quantity
        products = dataframe_products.groupby('Description')['Quantity'].sum(numeric_only=False)
        # Sort products by quantity, but since it's negative we sort in ascending order
        products = products.sort_values(ascending=True)
        # Plot the top 10 returned products
        ax = products.iloc[:10].plot(kind='bar')
        ax.invert_yaxis()
        plt.xlabel('Quantity Returned')
        plt.ylabel('Product')
        plt.title('Top 10 Returned Products')
        plt.savefig(f'modelisation/{id}.png', bbox_inches='tight')
    
    def plot_top_customers(self, id):
        # Group the data by customer and sum the Quantity
        customers = self.df.groupby('CustomerID')['Quantity'].sum(numeric_only=False)
        # Sort the customers by quantity
        customers = customers.sort_values(ascending=False)
        # Plot the top 10 customers
        customers.head(10).plot(kind='bar')
        plt.xlabel('Customer ID')
        plt.ylabel('Quantity Purchased')
        plt.title('Top 10 Customers by Quantity Purchased')
        plt.savefig(f'modelisation/{id}.png', bbox_inches='tight')

    def plot_top_products_by_country(self, id, country=None):
        # Only get rows where quantity is greater than zero (to ignore returns)
        df = self.df[self.df['Quantity'] > 0]
        countries = df['Country'].unique()
        if country:
            if country not in countries:
                print(f"Country '{country}' not found in data.")
                return
            countries = [country]
        for country in countries:
            # Filter data to include only rows for current country
            df_country = df[df['Country'] == country]
            # Group by product and sum the quantity
            products = df_country.groupby('Description')['Quantity'].sum(numeric_only=False)
            # Sort products by quantity
            products = products.sort_values(ascending=False)
            # Plot the top 10 products
            products.iloc[:10][:10].plot(kind='bar')
            plt.xlabel('Product')
            plt.ylabel('Quantity Sold')
            plt.title('Top 10 Sold Products in {}'.format(country))
            plt.savefig(f'modelisation/{id}.png', bbox_inches='tight')

    def plot_customer_purchases_in_period(self, customer_id, start_date, end_date, id, product_name=None):
        # Filter dataframe by customer ID
        df = self.df[self.df['CustomerID'] == customer_id]
        # Filter dataframe by date
        df = df[(df['InvoiceDate'] >= start_date) & (df['InvoiceDate'] <= end_date)]
        # Filter dataframe by product name
        if product_name:
            df = df[df['Description'] == product_name]
        # Create a column with the month of the purchase
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
        df['month'] = df['InvoiceDate'].dt.to_period('M')
        # Group by month and sum the Quantity
        purchases = df.groupby('month')['Quantity'].sum()
        # Plot purchases by month
        if product_name:
            title = 'Purchases of {} by Month'.format(product_name)
        else:
            title = 'Total Purchases by Month'
        purchases.plot(kind='bar', title=title)
        plt.xlabel('Month')
        plt.ylabel('Quantity Purchased')
        plt.savefig(f'modelisation/{id}.png', bbox_inches='tight')
