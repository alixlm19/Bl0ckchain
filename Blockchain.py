from Block import Block

class Blockchain:

    def __init__(self):
        self.chain = [Block()]

    def addTransaction(self, nonce, sender, receiver, quantity):
        """
        Adds a transaction to the last block. If the block is full
        a new block is created with the last transaction.
        """
        if(self.chain[-1].isFilled()):
            self.__addBlock()
        self.chain[-1].addTransaction(nonce, sender, receiver, quantity)            

    def __addBlock(self):
        """
        Adds a block to the chain.
        """
        self.chain.append(Block(self.chain[-1]))

    def verifyIntegrity(self, quickCheck = False):
        print(self.checkBlock())
        print(self.checkTransaction())

    def checkBlock(self):
        for i in range(1, len(self.chain)):
            prevBlockHash = self.chain[i - 1].getBlockHash()
            
            #Checks if the previous block hash is not equal to the current block hash
            for transaction in self.chain[i].transactionList:
                if(transaction["prevBlockHash"] != prevBlockHash):
                    print("Invalid block")
                    return False
        return True

    def checkTransaction(self):
        for block in self.chain:
            for i in range(1, block.getBlockTransactionCount()):
                prevTrans = block.transactionList[i - 1]
                currTrans = block.transactionList[i]
                if(prevTrans["hash"] != currTrans["prevTransHash"]):
                    
                    print("Invalid transaction")
                    return False
                if(prevTrans["hash"] != block.getRawTransactionHash(i - 1)):
                    print("Invalid transaction\n\n" + str(prevTrans))
                    return False
        return True

    def __removeBlock(self, index):
        pass

    def __str__(self):
        str_ = ""
        for block in self.chain:
            str_ += str(block)
        return str_

b = Blockchain()
b.addTransaction(0, "Alix", "Leon", 1)
b.addTransaction(1, "Francisco", "Leon", 1)
b.addTransaction(2, "Josefina", "Montesino", 1)
b.addTransaction(3, "Alicia", "Leon", 1)

#print(b)
#b.checkBlock()
#print(b.checkTransaction())
#b.chain[0].transactionList[0]["quantity"] = 2
b.verifyIntegrity()
