from flask_sqlalchemy import SQLAlchemy
 
db = SQLAlchemy()
 
class BookModel(db.Model):
    __tablename__ = 'books'
 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Integer())
    author = db.Column(db.String(80))
 
    def __init__(self, name, price, author):
        self.name = name
        self.price = price
        self.author = author 
     
    def json(self):
        return {"name":self.name, "price":self.price, "author":self.author}
