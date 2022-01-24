from main import db

class Products(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    image = db.Column(db.String(100), unique=False)

product1 = Products(name='one', image="/static/images/sticker_1.png")
product2 = Products(name='two', image="/static/images/sticker_2.png")
product3 = Products(name='three', image="/static/images/sticker_7.jpg")
product4 = Products(name='four', image="/static/images/sticker_4.png")
product5 = Products(name='five', image="/static/images/sticker_5.png")
product6 = Products(name='six', image="/static/images/sticker_11.jpg")
product7 = Products(name='seven', image="/static/images/sticker_10.jpg")
product8 = Products(name='eight', image="/static/images/sticker_6.png")


db.session.add(product1)
db.session.add(product2)
db.session.add(product3)
db.session.add(product4)
db.session.add(product5)
db.session.add(product6)
db.session.add(product7)
db.session.add(product8)
db.session.commit()

