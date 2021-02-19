import time

from sqlite3 import Error
import sqlite3

from datetime import datetime

from Mail import Send_Email

from Amazon import Amazon

#TODO: Do a better job on filtering sale prices from current price
#TODO: Readd infinite loop until the price has gone on sale
#TODO: Reimplement other functions while keeping code optimizes
#TODO: Readd notification of when product goes on sale

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

#def notify_user(current_price, on_sale, user_choice, product_title, product_URL):
    #If the current press is less than or equal to the user's desired price, choose how to notify the user
    #if(on_sale):
        #If the user inputted an email, than email them, else log to console the fallen price
       # if(user_choice is not None):
        #    Send_Email(user_choice, "{} is on sale".format(product_title), "The item you have wished for us to track has gone on sale to a price of: ${}, buy it at: {}".format(current_price, product_URL))
        #else:
            #print("The item you have tracked is currently on sale for a price of {}, buy it at: {}".format(current_price, product_URL))


def main_extract(URL, desired_price, user_choice):

    #Creation of an Amazon object
    product = Amazon(URL)

    #Collects the product's information and stores it into the object
    product.collectInformation()

    #Output of product's information
    product.toString()
    
    #After finding the individual element of each item, call main
    main(product.productInformation['Title'], product.productInformation['Price'], product.productInformation['Sale'])

    #After adding the results to the console, email the user if they specified for an email else log in the console if the product is on sale
    #notify_user(result[1], result[2], user_choice, result[0], URL)

#Creation of a database to store all excess data

def create_connection(db_file):

    conn = None

    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    
    return conn

def create_task(conn, task):
    sql = 'INSERT INTO AmazonData(unix, datestamp, title, price) VALUES (?, ?, ?, ?)'

    cur = conn.cursor()
    cur.execute(sql, task)

    return cur.lastrowid

def main(product_title, price, sale):
    database = r"Storage.db"

    conn = create_connection(database)

    unix = time.time()
    with conn:
        #Since a product's price can be changed even without going on sale, it's good to store it in the db
        Data = (unix, str(datetime.datetime.fromtimestamp(unix).strftime(' %Y-%m-%d %H: %M: %S '), product_title, price, str(sale)))
        
        create_task(conn, Data)
        print("Added data to Amazon_Storage table")


if __name__ == "__main__":

    #Prompts for all data needed and checking for invalid email responses
    information = collect_Information()

    main_extract(information[0], information[1], information[2])

