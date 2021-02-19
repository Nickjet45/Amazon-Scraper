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
        #Creates a dictionary to store the product's information, initalzing each value to an empty string, -1, or false
        self.productInformation = {"Title": "", "Price": "","Rating": "","Reviews": "", "Sale": False}

        #Initializes the private soup variable
        self.__SoupStartup()

        #Retrieves each individual item by parsing through the html, and assigns the item to a specific index of the tuple productInformation

        #Finds the product's Title and stores it into the dictionary
        self.productInformation['Title']= self.__soup.find('span', 'a-size-large product-title-word-break').text.strip()

        #Finds the product's current price and stores it within the dictionary
        self.productInformation['Price'] = self.__soup.find('span', 'a-size-medium a-color-price priceBlockBuyingPriceString').text.strip()

        #Retrieves the current star rating and adds it to the dictionary
        self.productInformation['Rating'] = self.__soup.find('span', 'a-icon-alt').text.strip()

        #Retrieves the number of reviews and adds it to the dictionary

        self.productInformation['Reviews'] = self.__soup.find('span', {"class": 'a-size-base', "id": "acrCustomerReviewText"}).text

        #Determines whether the product is currently on sale and if it is create a new element in the dictionary for Sale Price
        try:
            price = self.soup.find('span', 'priceBlockStrikePriceString a-text-strike').text.strip()

            self.productInformation['SalePrice'].append(price)

            self.productInformation['Sale'] = True
        #If the above code throws an exception, than the product is currently not on sale
        except AttributeError:
            self.productInformation['Sale'] = False

        #After collecting information, close the driver
        self.__EdgeClose()

    #Method to neatly output the user informaton
    def toString(self):
        #Loops over the dictionary to allow nice output
        for k, v in self.productInformation.items():
            #If the key SalePrice exists in the dictionary, than the product is on sale and the output needs to be changed
            if("SalePrice" in self.productInformation):
                #If the current key being evulated is Price, then change the output to "Original Price"
                if(k == "Price"):
                    print("Original Price: " + v)
                
                elif(k== "Sale"):
                    print("On Sale: " + str(v))
                
                elif(k == "SalePrice"):
                    print("Current Price: " + v)
                else:
                    print(k + ": " + v)

            #Else the product is not on sale and use this print format
            else:
                #If the current key is Price, change the output to "Current Price: " v, and if it's sale change it to "On Sale: " v, else leave it as it is
                if(k == "Price"):
                    print("Current Price: " + v)

                elif(k == "Sale"):
                    print("On Sale: "+ str(v))

                else:
                    print(k + ": " + v)

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