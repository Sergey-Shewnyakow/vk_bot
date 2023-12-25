import datetime

from peewee import *

db = SqliteDatabase('data.db')


class User(Model):
    class Meta:
        database = db
        db_table = 'User'
    vk_id = IntegerField()
    warns = IntegerField()

class Msg(Model):
    class Meta:
        database = db
        db_table = 'Msg'
    vk_id = IntegerField()
    msg = TextField()

class Imp_Msg(Model):
    class Meta:
        database = db
        db_table = 'Imp_Msg'
    vk_id = IntegerField()
    msg = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

if __name__ == '__main__':
    db.create_tables([User, Msg, Imp_Msg])