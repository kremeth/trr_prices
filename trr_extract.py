from selenium.webdriver.firefox.options import Options
import flask
import re
import string
import sys
from collections import namedtuple as _namedtuple
import pymysql
import ssl
import time
from selenium import webdriver
import re
import pandas as pd
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
from tqdm import tqdm
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from scrapingbee import ScrapingBeeClient




ssl._create_default_https_context = ssl._create_unverified_context

connection = pymysql.connect(
    host='34.142.176.229', user='root', password='HAM1qzn-gyt7pae-agj', db='stylebase')
cursor = connection.cursor()

cursor.execute('SELECT reference_field FROM Items;')
comp = '|||'.join([val[0] for val in cursor.fetchall()])

app = flask.Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return "waiting"


@app.route('/<string:name>')
def get_closest_utils(name):


    client = ScrapingBeeClient(api_key='BM5Q0NT8RSPM2HQJH0QZM7X2BSOL1V6QQ7M7PD8O18708DSGQZH59QBTG566QUTKEWJKOPFWMIYHS2JI')

    response = client.get(f"https://www.therealreal.com/products?keywords={name}",
        params = { 
            'render_js': 'False',
            'premium_proxy': 'True',
            'stealth_proxy': 'True'
        }
    )

    r_text = str(response.content)
    containers = r_text.split('><a class="product-card js-plp-product-card " data-container-number=""')[1:]
    images = [val.split('src="')[1].split('" srcset')[0] for val in containers]
    brands = [val.split('product-card__brand">')[-1].split('</div')[0] for val in containers]
    descriptions = [val.split('product-card__description">')[-1].split('</div')[0] for val in containers]




    prices = []
    for val in containers:
        try:
            prices.append(float(val.split('product-card__price">')[-1].split('</div')[0].split('<span class="sr-only"> - Price: </span>')[-1].split('- Price:\n')[-1].split('$')[-1].replace(',', '')))
        except:
            prices.append(float(val.split('product-card__discount-')[-1].split(' - </span>')[-1].split(' - ')[1].split('<span')[0].split('$')[-1].replace(',', '')))


    retail_prices = []
    for val in containers:
        try:
            retail_prices.append(float(val.split('product-card__msrp">Est. Retail\\xc2\\xa0')[-1].split('</div>')[0].split('$')[-1].replace(',', '')))
        except:
            retail_prices.append('NA')

    # return 'nailed it'

    return pd.DataFrame(list(zip(images, brands, descriptions, prices, retail_prices)), columns = ['image', 'brand', 'model', 'price', 'retail price']).to_json()



if __name__ == "__main__":
    app.secret_key = 'ItIsASecret'
    app.debug = True
    app.run()



# client = ScrapingBeeClient(api_key='BM5Q0NT8RSPM2HQJH0QZM7X2BSOL1V6QQ7M7PD8O18708DSGQZH59QBTG566QUTKEWJKOPFWMIYHS2JI')


# response = client.get("https://www.therealreal.com/products?keywords=saddle",
#     params = { 
#         'render_js': 'False',
#         'premium_proxy': 'True',
#         'stealth_proxy': 'True'
#     }
# )

# r_text = str(response.content)
# containers = r_text.split('><a class="product-card js-plp-product-card " data-container-number=""')[1:]
# images = [val.split('src="')[1].split('" srcset')[0] for val in containers]
# brands = [val.split('product-card__brand">')[-1].split('</div')[0] for val in containers]
# descriptions = [val.split('product-card__description">')[-1].split('</div')[0] for val in containers]




# prices = []
# for val in containers:
#     try:
#         prices.append(float(val.split('product-card__price">')[-1].split('</div')[0].split('<span class="sr-only"> - Price: </span>')[-1].split('- Price:\n')[-1].split('$')[-1].replace(',', '')))
#     except:
#         prices.append(float(val.split('product-card__discount-')[-1].split(' - </span>')[-1].split(' - ')[1].split('<span')[0].split('$')[-1].replace(',', '')))


# retail_prices = []
# for val in containers:
#     try:
#         retail_prices.append(float(val.split('product-card__msrp">Est. Retail\\xc2\\xa0')[-1].split('</div>')[0].split('$')[-1].replace(',', '')))
#     except:
#         retail_prices.append('NA')

# pd.DataFrame(list(zip(images, brands, descriptions, prices, retail_prices)), columns = ['image', 'brand', 'model', 'price', 'retail price']).to_string()








