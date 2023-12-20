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

if __name__ == '__main__':
    db.create_tables([User, Msg])