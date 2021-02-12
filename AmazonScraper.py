from bs4 import BeautifulSoup

import time

from sqlite3 import Error
import sqlite3

from datetime import datetime

from Mail import Send_Email

from msedge.selenium_tools import Edge, EdgeOptions
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

#Beginning of rework
def extract_Amazon_information(URL):
    


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
    database = r"SQLITE Database path"

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

    URL = input('What is the URL of the item? ')
    given_price = int(input('What price would you like to be notified at, rounded to the nearest dollar? '))
    user_email = input('Would you like to be emailed at your desired price?[Y/N] ')
    Valid_Email(user_email)

