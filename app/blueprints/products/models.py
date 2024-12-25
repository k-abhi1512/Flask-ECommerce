from app.extensions import mongo
from bson.objectid import ObjectId

class Product:
    def __init__(self, name, description, price, quantity, image, _id=None):
        self.name = name
        self.description = description
        self.price = float(price)
        self.quantity = quantity
        self.image = image  # Store the image path
    
    def save_to_db(self):
        product = {
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'quantity': self.quantity,
            'image_path': self.image
        }
        result = mongo.db.products.insert_one(product)
        self._id = result.inserted_id
        return self
    
    @staticmethod
    def get_all():
        return mongo.db.products.find()
    
    @staticmethod
    def get_by_id(product_id):
        return mongo.db.products.find_one({'_id': ObjectId(product_id)})
    
    @staticmethod
    def update_product(product_id, updated_data):
        mongo.db.products.update_one({'_id': ObjectId(product_id)}, {'$set': updated_data})
    
    @staticmethod
    def delete_product(product_id):
        mongo.db.products.delete_one({'_id': ObjectId(product_id)})
