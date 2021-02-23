import time

from sqlite3 import Error
import sqlite3

import datetime

from Mail import Send_Email

from Amazon import Amazon

import matplotlib.pyplot as plt

from matplotlib import style

style.use('fivethirtyeight')

#TODO: Do a better job on filtering sale prices from current price
#TODO: Readd infinite loop until the price has gone on sale
#TODO: Reimplement other functions while keeping code optimizes
#TODO: Readd notification of when product goes on sale

#Collects the user information such as email, URL of the item they wish to track, and the price that they wish to be notified at
def collect_Information():
    URL = input("What is the URL of the item you wish to track? ")

    desired_price = int(input('What price would you like to be notified at, rounded to the nearest dollar? '))

    user_email = Desires_Email()

    repeat_desire = input("Would you like to loop until the product is on sale? [Y/y] anything else is no? ").upper()

    #Returns a tuple of information for the program to use as needed

    return (URL, desired_price, user_email, repeat_desire)

#Ask the user if they would like to be emailed, if yes ask them for their email, else move along in the program
def Desires_Email():
    userChoice = input("Would you like to be emailed? [Y/N] ")

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

#Creation of a database to store all excess data

def create_connection(db_file):

    conn = None

    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    
    return conn

def create_task(conn, task):
    sql = 'INSERT INTO AmazonData(unix, datestamp, title, price, sale) VALUES (?, ?, ?, ?, ?)'

    cur = conn.cursor()
    cur.execute(sql, task)

    return cur.lastrowid

#Graphs the data from the database, with the connection to the database being passed through the function
def graph_data(conn, title):
    c = conn.cursor()

    #Make sure to limit the select statement to a specific product
    sql = 'SELECT unix, price FROM AmazonData WHERE title = "{}"'.format(title)
    c.execute(sql)

    dates = []
    values = []

    #Loops over the values retrieved and stores them into the database as the data is read in
    for row in c.fetchall():
        dates.append(datetime.datetime.fromtimestamp(row[0]))
        
        values.append(row[1])
    
    #After all the data is read in, create a line graph and than show it
    plt.plot_date(dates, values, '-')
    plt.title(title)
    plt.show()

def main_extract(URL, desired_price, user_choice, loopDesire):

    #Creation of an Amazon object
    product = Amazon(URL, 'Edge')

    #Collects the product's information and stores it into the object
    product.collectInformation()

    #Output of product's information
    product.toString()
    
    #After finding the individual element of each item, call main
    main(product.title, product.current_price, product.sale_status)

    #After adding the results to the console, email the user if they specified for an email else log in the console if the product is on sale
    #notify_user(result[1], result[2], user_choice, result[0], URL)
    if(loopDesire == "Y" and product.sale_status is False):
        loopFunction(URL, desired_price, user_choice)

def main(product_title, price, sale):
    database = r"Storage.db"

    conn = create_connection(database)

    unix = time.time()
    with conn:
        #Since a product's price can be changed even without going on sale, it's good to store it in the db
        Data = (unix, str(datetime.datetime.fromtimestamp(unix).strftime(' %Y-%m-%d %H: %M: %S ')), product_title, price, str(sale))

        create_task(conn, Data)
        print("Added data to Database")
    #graph_data(conn, product_title)

def loopFunction(URL, desired_price, user_choice):
    #Sleeps for a day, and then reruns main
    print("Going to sleep")
    time.sleep(43200)
    print("Sleep half done")
    time.sleep(43200)
    print("Rechecking product's information")

    main_extract(URL, desired_price, user_choice, "Y")

if __name__ == "__main__":

    #Prompts for all data needed and checking for invalid email responses
    information = collect_Information()

    main_extract(information[0], information[1], information[2], information[3])

