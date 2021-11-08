from app import db
from flask_login import UserMixin # Use only for the a USER model
from datetime import datetime as dt, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
import secrets
from app.blueprints.shop.models import Cart, Item



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(200), unique=True, index=True)
    password = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    cart = db.relationship('Cart', cascade='all, delete-orphan', backref='user')
    c_cart_items=[]

    token = db.Column(db.String, index=True, unique=True)
    token_exp = db.Column(db.DateTime)
    is_admin = db.Column(db.Boolean, default=False)

    ##################################################
    ############## Methods for Token auth ############
    ##################################################

    def get_token(self, exp=86400):
        current_time = dt.utcnow()
        # give the user their token if the token is not expired
        if self.token and self.token_exp > current_time + timedelta(seconds=60):
            return self.token
        # if not a token create a token and exp date
        self.token = secrets.token_urlsafe(32)
        self.token_exp = current_time + timedelta(seconds=exp)
        self.save()
        return self.token

    def revoke_token(self):
        self.token_exp = dt.utcnow() - timedelta(seconds=61)

    @staticmethod
    def check_token(token):
        u = User.query.filter_by(token=token).first()
        if not u or u.token_exp < dt.utcnow():
            return None
        return u

    #########################################
    ############# End Methods for tokens ####
    #########################################

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data["email"]
        self.password = self.hash_password(data['password'])

    #salts and hashes our password to make it hard to steal
    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    # compares the user password to the password provided in the login form
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    # saves the user to the database
    def save(self):
        db.session.add(self) # add the user to the db session
        db.session.commit() #save everything in the session to the database

    def __repr__(self):
        return f'<User: {self.id} | {self.email}>'

    def my_cart(self):
        my_cart = Cart.query.filter_by(user_id=self.id)
        return my_cart

    def my_cart_items(self):
        if len(self.c_cart_items)==Cart.query.filter(Cart.user_id==self.id).count():
            return self.c_cart_items
        my_items=[]
        items=db.session.query(Item.id).join(Cart,Cart.item_id==Item.id).filter(Cart.user_id==self.id).all()
        all_items=Item.query.all()
        for citem in items:
            for item in all_items:
                if citem[0]==item.id:
                    my_items.append(item)
        self.c_cart_items=my_items[:]
        return self.c_cart_items

    def my_cart_items_unique(self):
        items=Item.query.join(Cart,Cart.item_id==Item.id).filter(Cart.user_id==self.id).all()
        return items

    def cart_total(self):
        total=0.00
        for item in self.my_cart_items():
            total+=item.price
        return total
    
    def cart_item_count(self):
        return(len(self.my_cart_items()))

    def empty_cart(self):
        ct=Cart.query.filter_by(user_id=self.id).all()
        for item in ct:
            item.remove()


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    
    # SELECT * FROM user WHERE id = ???
