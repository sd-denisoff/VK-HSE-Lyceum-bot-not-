from peewee import *


db = SqliteDatabase('database.db')


class User(Model):
    id = CharField(primary_key=True)
    role = TextField(default='user')
    token = TextField(null=True, default=None)
    group = TextField(null=True, default=None)
    eljur_id = TextField(null=True, default=None)
    date = TextField(default='')

    @staticmethod
    def get_groups():
        users = User.select()
        groups = list()
        groups.append(('all', 'Всем'))
        for user in users:
            option = (user.group, user.group)
            groups.append(option)
        return set(groups)

    class Meta:
        database = db
        db_table = 'Users'


class Review(Model):
    text = TextField()
    date = TextField()
    was_read = BooleanField(default=False)

    class Meta:
        database = db
        db_table = 'Reviews'


class BadQnA(Model):
    qn = TextField()
    answer = TextField()

    class Meta:
        database = db
        db_table = 'BadQnA'
