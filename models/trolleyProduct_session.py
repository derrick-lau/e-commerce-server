from flask import session
from models.product import Product
import json

class SessionTrolleyProduct():

    def __init__(self, productId, quantity, userId):
        self.productId = productId
        self.quantity = quantity
        self.userId = userId
    
    def json(self):
        product = Product.findById(self.productId)
        return {
            "productId":self.productId,
            "productName":product.productName,
            "image":product.image,
            "price":product.price,
            "quantity":self.quantity,
            "total":product.price * self.quantity,
    }

    @classmethod 
    def getTrolleyProducts(cls, userId):
        
        trolleyProducts = {}
        if f'{userId}' in session:
      
            productIdList = session[f'{userId}']
            for productId in productIdList:
                if productId in trolleyProducts:
                    trolleyProduct = trolleyProducts[productId]
                    trolleyProduct.setQuantity(trolleyProduct.getQuantity() + 1)
                else:
                    trolleyProducts[productId] = SessionTrolleyProduct(productId, 1, userId)

            return trolleyProducts

        else:
            return trolleyProducts
   
   
    def add(self):
        if f'{self.userId}' not in session:
            session[f'{self.userId}'] = []
        trolley = session[f'{self.userId}']
        trolley.append(self.productId)
        session[f'{self.userId}'] = trolley
      

    @classmethod 
    def delete(cls, self, isBreak: bool):
        productIdList = session[f'{self.userId}']
        newList = list.copy(productIdList)
        for productId in productIdList:
            if(productId == self.productId):
                newList.remove(productId)
                if isBreak:
                    break
        session[f'{self.userId}'] = newList

    def deleteOne(self):
        self.delete(self, True)

    def deleteAll(self):
        self.delete(self, False)

    def getQuantity(self):
        return self.quantity

    def setQuantity(self, quantity):
        self.quantity = quantity


