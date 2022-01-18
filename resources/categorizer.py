import re
import resources.webbot as webbot
import resources.ofx_parser as ofx_parser
import datetime as dt
from data.associations import data

class Categorizer:
    def __init__(self):
        self.names = list() #array of names (memos)
        self.values = list() #array of dollar values
        self.category = list() #an array of categories
        self.dates = list() #an array of dates
        self.scores = list(list()) #a double list that keeps track of the point totals for each transaction

    def extract_data(self, ofx_parser):
        #for each transaction in our input
        for i, data in enumerate(ofx_parser.types):
            if (data == "debit"):
                s = str(ofx_parser.dates[i]).split(' ') #split the transaction such that we obtain the information we want
                self.dates.append(s[0])
                self.values.append(ofx_parser.amounts[i])
                self.names.append(ofx_parser.memos[i])
        
        web_contents = list() #an array of each net_output string from webbot
        #for each transaction get the name
        for transaction in self.names:
            bot = webbot.Webbot()
            #extract the text with the bot
            bot.query_text(transaction)
            bot.strip_text()
            web_contents.append(bot.net_output)
        
        #categorize the transactions
        self.categorize(web_contents)

    def categorize(self, web_contents):
        for i, content in enumerate(web_contents):
            #use keywords to replace text
            replacement = self.multiple_replace(content, data[0]) 
            replacement = self.multiple_replace(replacement, data[1])
            replacement = self.multiple_replace(replacement, data[2])
            replacement = self.multiple_replace(replacement, data[3])
            replacement = self.multiple_replace(replacement, data[4])

            #count the occurences (score) for each category
            transportation = replacement.count('transportation')
            housing = replacement.count('housing')
            food = replacement.count('food')
            entertainment = replacement.count('entertainment')
            education = replacement.count('education')
            
            # transportation = self.score_category(content, data[0])
            # housing = self.score_category(content, data[1])
            # food = self.score_category(content, data[2])
            # entertainment = self.score_category(content, data[3])
            # education = self.score_category(content, data[4])

            #create array of the scores for a given category
            totals = [food, entertainment, housing, transportation, education]
            self.scores.append(totals)
            
            #determine which category
            if (food > entertainment and food > housing and food > transportation and food > education):
                self.category.append("Food")
            elif (entertainment > food and entertainment > transportation and entertainment > education and entertainment > housing):
                self.category.append("Entertainment")
            elif (housing > food and housing > entertainment and housing > education and housing > transportation):
                self.category.append("Housing")
            elif (transportation > food and transportation > education and transportation > entertainment and transportation > housing):
                self.category.append("Transportation")
            elif (education > food and education > transportation and education > housing and education > entertainment):
                self.category.append("Education")
            else:
                self.category.append("Misc.")

    # def score_category(self, content, associations):
    #     count = 0
    #     for association in associations:
    #         count += content.count(association[0])
    #     return count
    
    
     #function to replace all occurenes using the dictionary passed in
    def multiple_replace(self, string, rep_dict):
         output = string
         try:
             pattern = re.compile("|".join([re.escape(k) for k in sorted(rep_dict,key=len,reverse=True)]), flags=re.DOTALL)
             output = pattern.sub(lambda x: rep_dict[x.group(0)], string)
         except:
             print("Multiple_replace failed")
         return output
        
