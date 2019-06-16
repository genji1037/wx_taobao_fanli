from peewee import *

db = MySQLDatabase('tbrobo', user='tbrobo', password='Cyy123456', host='localhost', port=3306)


class User(Model):  # 主键是wx备注
    balance = DecimalField()
    total_amt = DecimalField()
    adzone_id = CharField()  # 推广位ID
    tb_id = CharField()  # 淘宝6位用户编号

    class Meta:
        database = db


class Order(Model):
    # order_no = CharField()
    uid = CharField()
    robot_bonus = DecimalField()
    user_bonus = DecimalField()
    state = CharField()  # create, confirm
    pay_time = DateTimeField()
    confirm_time = DateTimeField()

    class Meta:
        database = db


class Withdraw(Model):
    uid = CharField()
    amount = DecimalField()
    state = CharField()  # apply, done
    apply_time = DateTimeField()
    done_time = DateTimeField()

    class Meta:
        database = db


class Adzone(Model):  # 推广位
    adzone_id = CharField()  # 推广位ID
    state = CharField()  # bind:已绑定, free:未绑定

    class Meta:
        database = db


def init():
    db.connect()
    db.create_tables([User, Order, Withdraw, Adzone])

