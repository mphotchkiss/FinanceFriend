import re 
from bs4 import BeautifulSoup
import urllib.request 
from googlesearch import search

class Webbot:
    def __init__(self):
        self.results = list() # this list stores all the text from the queries
        self.net_output = "" # this string stores all of the text (excludes white space)

    def query_text(self, query): 
        # for each result in the search, start at the first and stop at the 3rd. Separate the queries 1 second apart.
        for j in search(query, tld="co.in", num=2, start=0, stop=2, pause=1):
            try:
                # make a request to open - abort if takes more than 10 seconds
                html = urllib.request.urlopen(j, timeout=10)
                soup = BeautifulSoup(
                    html, features="html.parser")  # create a parser
                data = soup.get_text()  # get the text from the HTML with the parser
                self.results.append(str(data))  # append the text to our results
            except:
                print("Failure occurred for search " + j)
    
    def strip_text(self):
        for result in self.results:
            # remove next line characters for each of the 3 results
            lines = result.split('\n')
            # remove all empty lines
            non_empty_lines = [line for line in lines if line.strip() != ""]
            text = ""  # string that will store the non-empty lines
            for line in non_empty_lines:
                text += line + '\n'  # add each non-empty line to our storage
            self.net_output += text  # append all of the text to our result
            self.net_output = self.net_output.lower()  # create the lower case string
