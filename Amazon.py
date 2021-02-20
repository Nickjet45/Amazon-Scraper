from bs4 import BeautifulSoup

from msedge.selenium_tools import Edge, EdgeOptions

#TODO: add support for other browsers, Ex. Chrome, FireFox, etc. 
#TODO: Try and optimize time it takes to retrieve informaton(possibly change to simply use requests)

class Amazon():
    #Initalizes the object to only have an instance variable for URL
    def __init__(self, URL):
        self.URL = URL
    
    #Collects the product's information and stores it into an instance variable of type dictionary
    def collectInformation(self):
        #Initializes the private soup variable
        self.__SoupStartup()

        #Retrieves each individual item by parsing through the html, and assigns the item to a specific index of the tuple productInformation

        #Finds the product's Title and stores it into a corresponding instance variable
        self.title = self.__soup.find('span', 'a-size-large product-title-word-break').text.strip()

        #Finds the product's current price and stores it into a corresponding instance variable
        self.current_price = self.__soup.find('span', 'a-size-medium a-color-price priceBlockBuyingPriceString').text.strip()

        #Retrieves the current star rating and adds it into a corresponding instance variable
        self.rating = self.__soup.find('span', 'a-icon-alt').text.strip()

        #Retrieves the number of reviews and adds it into a corresponding instance variable

        self.review_count = self.__soup.find('span', {"class": 'a-size-base', "id": "acrCustomerReviewText"}).text

        #Determines whether the product is currently on sale and if it is create a new element in the dictionary for Sale Price
        try:
            price = self.__soup.find('span', 'priceBlockStrikePriceString a-text-strike').text

            self.sale_price = price

            self.sale_status = True

        #If the above code throws an exception, than the product is currently not on sale
        except AttributeError:
            self.sale_status = False

        #After collecting information, close the driver
        self.__EdgeClose()

    #Method to neatly output the user informaton
    def toString(self):
        
        #If the item is on sale, use X output format, else use Y output

        if self.sale_status:
            #Prints the title of the product
            print("Product: " + self.title)

            #Prints that the product is currently on sale
            print("On Sale: " + str(self.sale_status))

            #Prints the current price of the product, followed by it's original price
            print("Current price: " + self.current_price)

            print("Original price: " + self.sale_price) 

            #Print the review count followed by the star rating
            print("Review Count: " + self.review_count)

            print("Rating: " + self.rating)
        
        else:
                        #Prints the title of the product
            print("Product: " + self.title)

            #Prints that the product is currently on sale
            print("On Sale: " + str(self.sale_status))

            #Prints the current price of the product
            print("Current price: " + self.current_price)

            #Print the review count followed by the star rating
            print("Review Count: " + self.review_count)

            print("Rating: " + self.rating)

    #Private instance method for class Amazon, as end user does not need to worry about retrieval of html content
    def __SoupStartup(self):
        #Starts up Selenium Driver
        self.__seleniumDriverStartup()

        #Stores the html content of the URL within the private instance variable named soup
        self.__soup = BeautifulSoup(self.__driver.page_source, 'html.parser')
    
    def __EdgeClose(self):
        self.__driver.quit()


    #Private method of class Amazon, as the user does not need to worry about Selenium driver for Edge
    def __seleniumDriverStartup(self):
        options = EdgeOptions()
        options.use_chromium = True

        self.__driver = Edge(options=options)

        self.__driver.get(self.URL)