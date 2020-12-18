from bs4 import BeautifulSoup
import requests
import time
from sqlite3 import Error
import sqlite3
from datetime import datetime

from Mail import Send_Email

#Email check written as function to loop through for invalid responses

def Valid_Email(email):
    if email == 'Y' or email == 'y':
        user_email = input('Please enter your email address. ')
    elif email == 'N' or email == 'n':
        print("You will not be notified by email. Check the console for updates ")
        user_email = None
    else:
        user_email = input("Invalid response, please enter Y or N: ")
        Valid_Email(user_email)

#Prompts for all data needed and checking for invalid email responses

URL = input('What is the URL of the item? ')
given_price = int(input('What price would you like to be notified at, rounded to the nearest dollar? '))
user_email = input('Would you like to be emailed at your desired price?[Y/N] ')
Valid_Email(user_email)

#User-Agent along with starting assumptions about the product to allow for easier data formatting

headers = {"User-Agent": 'Enter User-Agent'}
on_sale = False

#Function to track Amazon Prices, does not include email due to it being optional

def Price_Track(URL, desired_price, given_email):

    global product_title
    global price
    global on_sale

    #Requesting the HTML of the page of the URL

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'lxml')

    #Parsing through the HTML to find given id tags that correlate to the named variables

    product_title = soup.find(id="productTitle").get_text().strip()

    #Checks multiple price tags, due to Amazon changing them between the 3

    try:
        current_price = soup.find(id="priceblock_ourprice").get_text()
    except AttributeError:
        try:
            current_price = soup.find(id="priceblock_dealprice").get_text()
        except AttributeError:
            try:
                current_price = soup.find(id="priceblock_saleprice").get_text()
                on_sale = True
            except AttributeError:
                current_price = None
    
    #Method to check to see if the item is on sale

    try:
        original_price = soup.find(class_="priceBlockStrikePriceString a-text-strike")
        if original_price is None:
            original_price = current_price
            on_sale = False
        else:
            original_price = soup.find(class_="priceBlockStrikePriceString a-text-strike").get_text()
            on_sale = True
    except Exception as e:
        print(e)
    
    #Changing the prices to a float value
    if current_price is not None:
        price = float(current_price[1:6])
        orig_price = float(original_price[2:4])
    else:
        price = None
        orig_price = None

    #Calculating the sale percentage, if it's on sale

    if on_sale is True:
        sale_percentage = ((price - float(current_price[2:6]))/float(original_price[2:6])) * 100
    else:
        sale_percentage = 0

    #Notification of user of the current price

    while price > desired_price:
        if not on_sale:
            print("{} is currently not on sale. Current price of the item is: ${}".format(product_title, price))
        else:
            print("{} is currently on sale, but it is above your desired price. \n Current Price of item is: ${}".format(product_title, price))
        main()
        print('Going to sleep')

        time.sleep(10800)
        print("Sleep is 50% complete")
        
        time.sleep(10800)
        print('Waking up....')
    
    if price <= desired_price:
        if user_email is None:
            print("{} is on sale! Original Price: ${} \n Current Price: ${} \n Sale Percentage: {}%".format(product_title, orig_price, price, sale_percentage))
            main()
        else:
            print("{} is on sale! Original Price: ${} \n Current Price: ${} \n Sale Percentage: {}%".format(product_title, orig_price, price, sale_percentage))
            Send_Email(given_price, "{} has gone on sale! It is currently at ${}, with an original price of ${}. Making the sale percentage {}%".format(product_title, price, orig_price, sale_percentage), URL)
            main()

#Creation of a database to store all excess data

def create_connection(db_file):

    conn = None

    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    
    return conn

def create_task(conn, task):
    sql = ''' INSERT INTO Amazon_Storage(Title, Price, Date, Sale) VALUES(?,?,?,?)'''

    cur = conn.cursor()
    cur.execute(sql, task)

    return cur.lastrowid

def main():
    database = r"Path to local database"

    conn = create_connection(database)
    with conn:
        if on_sale:
            Data = (product_title, price, str(datetime.date(datetime.now())), 'True')
        else:
            Data = (product_title, price, str(datetime.date(datetime.now())), 'False')
        create_task(conn, Data)
        print("Added data to Amazon_Storage table")


Price_Track(URL, given_price, user_email)