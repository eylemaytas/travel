from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class City(db.Model, SerializerMixin):
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False) 
    language = db.Column(db.String, nullable=False)
    climate = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default = datetime.now)
    updated_at = db.Column(db.Datetime, default=datetime.now, onupdate=datetime.now)

#Relationships
destination = db.relationship('Destination', back_populates = 'city', cascade='all, delete-orphan')
foods = association_proxy('destinations', 'food', creator=lambda f: Destination(food=f))

#Serializer 
serialize_rules = ('-destinations')

#Validations

class Food(db.Model, SerializerMixin):
    __tablename__ = 'foods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    restaurant_recommendation = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default = datetime.now)
    updated_at = db.Column(db.Datetime, default=datetime.now, onupdate=datetime.now)
    


#Relationships
destinations = db.relationship('Destination', back_populates='foods', cascade='all, delete-orphan')
continent = db.relationship('Continent', back_populates = 'foods', cascade='all, delete-orphan')
cities = association_proxy('destinations', 'city ', creator=lambda c: Destination(city=c))


#Serializer 
serialize_rules = ('-destinations', '-city')

#Validations

class Destination(db.Model, SerializerMixin):
    __tablename__ = 'destinations'

    id = db.Column(db.Integer, primary_key=True)

    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'))

#Relationships
food = db.relationship('Food', back_populates='destinations')
city = db.relationship('City', back_populates='destinations')

#Serializer 
serialize_rules = ('-food', '-city')

#Validations

class Continent(db.Model, SerializerMixin):
    __tablename__ = 'continents'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'))

#Relationships
foods = db.relationship('Food', back_populates='continent',cascade='all, delete-orphan')
cities = db.relationship('City', back_populates='continent', cascade='all, delete-orphan')


#Serializer 
serialize_rules = ('-foods', '-cities')

#Validations

class Blog(db.Model, SerializerMixin):
    __tablename__ = 'blogs'

    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String, nullable=False)
    blog_post = db.Column(db.String, nullable=False)
    like_count = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default = datetime.now)
    updated_at = db.Column(db.Datetime, default=datetime.now, onupdate=datetime.now)
    
    user_id = db.Column(db.Integer, db.ForeingKey('users.id'))

#Relationships
user = db.relationship('User', back_populates='blog', cascade='all, delete-orphan')

#Serializer 
serialize_rules = ('-user',)

#Validations

class User(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default = datetime.now)
    updated_at = db.Column(db.Datetime, default=datetime.now, onupdate=datetime.now)

    
#Relationships
blogs = db.relationship('Blog', back_populates='user', cascade='all, delete-orphan')

#Serializer 
serialize_rules = ('-blogs',)

#Validations



# class Destination(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
#     city = db.relationship('City', backref='destinations')

# class City(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     image = db.Column(db.String)
#     language = db.Column(db.String)
#     climate = db.Column(db.String)
#     created_at = db.Column(db.DateTime)
#     updated_at = db.Column(db.DateTime)
#     continent_id = db.Column(db.Integer, db.ForeignKey('continents.id'))
#     continent = db.relationship('Continent', backref='cities')

# class Food(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     image = db.Column(db.String)
#     description = db.Column(db.String)
#     restaurant_recommendation = db.Column(db.String)
#     created_at = db.Column(db.DateTime)
#     updated_at = db.Column(db.DateTime)
#     continent_id = db.Column(db.Integer, db.ForeignKey('continents.id'))
#     destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'))
#     continent = db.relationship('Continent', backref='foods')
#     destination = db.relationship('Destination', backref='foods')

# class Continent(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     image = db.Column(db.String)
#     food_id = db.Column(db.Integer, db.ForeignKey('foods.id'))

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String)
#     last_name = db.Column(db.String)
#     username = db.Column(db.String)
#     password = db.Column(db.String)
#     created_at = db.Column(db.DateTime)
#     updated_at = db.Column(db.DateTime)

# class Blog(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     image = db.Column(db.String)
#     blog_post = db.Column(db.String)
#     like_count = db.Column(db.Integer)
#     created_at = db.Column(db.DateTime)
#     updated_at = db.Column(db.DateTime)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     user = db.relationship('User', backref='blogs')
