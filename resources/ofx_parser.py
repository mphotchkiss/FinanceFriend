from ofxparse import OfxParser

class OFX_Parser:
    def __init__(self, path):
        self.types = list()
        self.dates = list()
        self.amounts = list()
        self.memos = list()
        self.file_path = path

    def parse(self):
    
        #open the file with a parser
        ofx = OfxParser.parse(open(self.file_path))
        
        #grab the account
        account = ofx.account

        #grab the statement
        statement = account.statement

        #for each transaction in the statement add the field to our lists
        for transaction in statement.transactions:
            self.types.append(transaction.type) #str
            self.dates.append(transaction.date) #datetime.datetime
            self.amounts.append(transaction.amount) #decimal.Decimal
            self.memos.append(transaction.memo) #str
        
        
