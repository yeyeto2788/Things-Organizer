from datetime import datetime

from sqlalchemy import desc
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from things_organizer import DB as database

tags = database.Table('thing_tag',
    database.Column('tag_id', database.Integer, database.ForeignKey('tag.id')),
    database.Column('thing_id', database.Integer, database.ForeignKey('thing.id'))
)


class Thing(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.Text, nullable=False)
    description = database.Column(database.String(300))
    user_id = database.Column(database.Integer,
                              database.ForeignKey('user.id'),
                              nullable=False)
    category_id = database.Column(database.Integer,
                                  database.ForeignKey('category.id'),
                                  nullable=False)
    storage_id = database.Column(database.Integer,
                                 database.ForeignKey('storage.id'),
                                 nullable=False)
    date = database.Column(database.DateTime,
                           default=datetime.utcnow)
    _tags = database.relationship('Tag',
                                  secondary=tags,
                                  backref=database.backref('things', lazy='dynamic'))
    category = database.relationship('Category',
                                     backref=database.backref('things', lazy='dynamic'))
    storage = database.relationship('Storage',
                                    backref=database.backref('things', lazy='dynamic'))

    @staticmethod
    def newest(num):
        return Thing.query.order_by(desc(Thing.date)).limit(num)

    @property
    def tags(self):
        return ",".join([t.name for t in self._tags])

    @tags.setter
    def tags(self, string):
        if string:
            self._tags = [Tag.get_or_create(name) for name in string.split(',')]

    def __repr__(self):
        return "<Thing %r>" % self.name


class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(80), unique=True, nullable=False)
    email = database.Column(database.String(120), unique=True, nullable=False)
    things = database.relationship('Thing', backref='user', lazy='dynamic')
    password_hash = database.Column(database.String)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    def __repr__(self):
        return "<User %r>" % self.username

    def __unicode__(self):
        return self.username


class Category(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(50), nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.name


class Storage(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(50), nullable=False)
    location = database.Column(database.String(120), nullable=False)

    def __repr__(self):
        return '<Storage %r>' % self.name


class Tag(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(25), nullable=False, unique=True, index=True)

    @staticmethod
    def get_or_create(name):
        try:
            return Tag.query.filter_by(name=name).one()
        except:
            return Tag(name=name)

    @staticmethod
    def all():
        return Tag.query.all()

    def __repr__(self):
        return self.name
