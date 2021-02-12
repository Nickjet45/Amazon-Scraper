from bs4 import BeautifulSoup

import time

from sqlite3 import Error
import sqlite3

from datetime import datetime

from Mail import Send_Email

from msedge.selenium_tools import Edge, EdgeOptions

#Collects the user information such as email, URL of the item they wish to track, and the price that they wish to be notified at
def collect_Information():
    URL = input("What is the URL of the item you wish to track? ")

    desired_price = int(input('What price would you like to be notified at, rounded to the nearest dollar? '))

    user_email = Desires_Email()

    #Returns a tuple of information for the program to use as needed

    return (URL, desired_price, user_email)

#Ask the user if they would like to be emailed, if yes ask them for their email, else move along in the program
def Desires_Email():
    userChoice = input("Would you like to be emailed? [y\Y] ")

    if(userChoice == 'y' or userChoice == 'Y'):
        user_email = input("What is your email? ")
    else:
        user_email = None
    
    return user_email

def notify_user(current_price, on_sale, user_choice, product_title, product_URL):
    #If the current press is less than or equal to the user's desired price, choose how to notify the user
    if(on_sale):
        #If the user inputted an email, than email them, else log to console the fallen price
        if(user_choice is not None):
            Send_Email(user_choice, "{} is on sale".format(product_title), "The item you have wished for us to track has gone on sale to a price of: ${}, buy it at: {}".format(current_price, product_URL))
        else:
            print("The item you have tracked is currently on sale for a price of {}, buy it at: {}".format(current_price, product_URL))


def main_extract(URL, desired_price, user_choice):

    #Turning on the selenium driver
    options = EdgeOptions()
    options.use_chromium = True

    driver = Edge(options=options)

    driver.get(URL)

    #Sets soup equal to the html content of the page based off of the URL entered by the user
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    #Stores the result in a tuple called result
    result = extract_Amazon_information(soup)

    #After finding the individual element of each item, call main
    main(result[0], result[1], result[2])

    #After adding the results to the console, email the user if they specified for an email else log in the console if the product is on sale
    notify_user(result[1], result[2], user_choice, result[0], URL)

def extract_Amazon_information(soup):

    #The price of the item is equal to the value located at this specific html tag
    current_price = soup.find('span', 'a-size-medium a-color-price priceBlockBuyingPriceString').text

    #The title of the product is the value located at this specific html tag
    title = soup.find('span', 'a-size-large product-title-word-break').text

    #Try to find the original price of the item, if it an attributeError is thrown, than it does not exist and the product is not on sale. Else it does exist, and the product is on sale
    try:
        current_price = soup.find('span', 'priceBlockStrikePriceString a-text-strike').text
        on_sale = True
    except AttributeError:
        on_sale = False

    results = (title, current_price, on_sale)

    return results


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

def main(product_title, price, on_sale):
    database = r"Database path"

    conn = create_connection(database)
    with conn:
        if on_sale:
            Data = (product_title, price, str(datetime.date(datetime.now())), 'True')
        else:
            Data = (product_title, price, str(datetime.date(datetime.now())), 'False')
        create_task(conn, Data)
        print("Added data to Amazon_Storage table")


if __name__ == "__main__":

    #Prompts for all data needed and checking for invalid email responses
    information = collect_Information()

    main_extract(information[0], information[1], information[2])

