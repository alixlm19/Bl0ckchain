import hashlib
import pickle
import json
import time

class Block:

    def __init__(self, prevBlock = None):
        self.TRANSACTION_LIMIT = 2      #Transaction limit per block
        self.transactionList = []       #List of transactions in the block
        self.lastTransaction = dict()   #Last transaction made
        self.prevBlock = prevBlock      #Previous block

    def addTransaction(self, nonce, sender, receiver, quantity):
        """
        Creates a transaction dictionary from a set of arguments and
        appends it to the transaction list self.transactionList.
        """
        if(len(self.transactionList) < self.TRANSACTION_LIMIT):
            self.lastTransaction = {"nonce" : nonce,
                                    "timestamp" : time.time(),
                                    "sender" : sender,
                                    "receiver" : receiver,
                                    "quantity" : quantity,                                    
                                    "transCount" : self.getBlockTransactionCount(),
                                    "prevBlockHash" : self.getPrevBlockHash(self.prevBlock),
                                    "prevTransHash" : self.getPreviousHash()}
            
            self.lastTransaction["hash"] = self.getTransactionHash(self.lastTransaction)
            self.transactionList.append(self.lastTransaction)

    def getRawTransactionHash(self, i):
        transaction = dict(list(self.transactionList[i].items())[:len(self.lastTransaction) - 1])
        return hashlib.sha3_256(json.dumps(transaction, sort_keys = True).encode()).hexdigest()

    def isFilled(self):
        """
        Returns True if the number of elements in self.transactionList
        is equal to the transaction List, else, False.
        """
        return len(self.transactionList) == self.TRANSACTION_LIMIT

    def getPrevBlockHash(self, b = None):
        """
        Calculates the hash of the previous Block given that
        one was passed as an argument.
        """
        if(b == None):
            return "0000000000000000000000000000000000000000000000000000000000000000"
        else:
            return hashlib.sha3_256(pickle.dumps(self.prevBlock)).hexdigest()

    def getPreviousHash(self):
        """
        Returns the hash of the previous transaction done in the current or previous
        block.

        - If there is a previous transaction in the block, prevHash is set to the hash
          of the previous transaction.
        - If there is no previous block, prevHash is set to zero.
        - If there is a previous block, prevHash is set to the last transaction.    
        """
        if(len(self.transactionList) == 0):
            if(self.prevBlock == None):
                return "0000000000000000000000000000000000000000000000000000000000000000"
            else:
                return self.prevBlock.transactionList[-1]["hash"] 
        else:
            return self.transactionList[-1]["hash"]
            
    #Move this method to the Blockchain.py file
    def getBlockHash(self):
        """
        Returns the hash of the current block.
        """
        return hashlib.sha3_256(pickle.dumps(self)).hexdigest()

    def getTransactionHash(self, b):
        """
        Return the hash of the current transaction.
        """
        return hashlib.sha3_256(json.dumps(b, sort_keys = True).encode()).hexdigest()

    def getTransactionsFromSender(self, sender):
        """
        Returns all of the transactions of a sender in the current block.
        """
        transactions = []
        for transaction in self.transactionList:
            if(transaction["sender"] == sender):
                transactions.append(transaction)
        return transactions

    def getBlockTransactionCount(self):
        """
        Returns the transaction quantity in self.transactionList
        """
        return len(self.transactionList)

    def __str__(self):
        """
        Returns the block transaction information
        """
        str_ = "\n[\n"
        for transaction in self.transactionList:
            str_ += "\t{\n"
            for item in transaction:
                str_ += "\t\t" + str(item) + ": " + str(transaction[item]) + "\n"
            str_ += "\t}\n"
        str_ += "]\n"
        return str_
    
