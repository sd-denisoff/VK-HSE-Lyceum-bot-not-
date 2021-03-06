from peewee import *

db = SqliteDatabase('database.db')

class User(Model):
    id = CharField(primary_key=True)
    token = TextField(null=True, default=None)
    login = TextField(null=True, default=None)
    password = TextField(null=True, default=None)
    date = TextField(default='')
    act = TextField(null=True)

    class Meta:
        database = db
        db_table = 'Users'


class Review(Model):
    author = TextField()
    text = TextField()

    class Meta:
        database = db
        db_table = 'Reviews'