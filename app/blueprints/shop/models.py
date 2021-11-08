from app import db
from datetime import datetime as dt
from flask_login import current_user
from sqlalchemy import and_


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    products = db.relationship('Item', cascade ='all, delete-orphan',  backref="category")

    def __repr__(self):
        return f'<Catergoy: {self.id} | {self.name}>'

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        data={
            "id": self.id,
            "name": self.name
        }
        return data

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    img = db.Column(db.String)
    created_on = db.Column(db.DateTime, index=True, default=dt.utcnow)
    category_id = db.Column(db.ForeignKey('category.id'))

    def __repr__(self):
        return f'<Item: {self.id} | {self.name}>'

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        data={
            'id':self.id,
            "name":self.name,
            "price":self.price,
            "img":self.img,
            "description":self.description,
            "category_id":self.category_id,
            "created_on":self.created_on,
        }
        return data

    def from_dict(self, data):
        for field in ["name","description","price","img","category_id"]:
            if field in data:
                setattr(self,field, data[field])

    def add_to_cart(self):
        cart=Cart()
        cart.add_item(self)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.ForeignKey('item.id'))
    user_id = db.Column(db.ForeignKey('user.id'))

    def from_dict(self, data):
        for field in ['item_id','user_id']:
            if field in data:
                setattr(self, field, data[field])

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()
    
    def add_item(self, item):
        data={
            'item_id': item.id,
            'user_id': current_user.id
        }
        self.from_dict(data)
        self.save()

    def remove_item(item_id):
        Cart.query.filter(and_(Cart.user_id==current_user.id,Cart.item_id==item_id)).first().remove()
    
    def __repr__(self):
        return f'<Cart: {self.id} | {self.user_id}...>'