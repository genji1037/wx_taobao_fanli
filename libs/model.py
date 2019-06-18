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
    trade_id = CharField()  # tb订单号
    adzone_id = CharField()  # 推广位ID
    uid = CharField()  # user表主键
    pay_price = DecimalField()
    tb_paid_time = DateTimeField()
    tk_order_role_text = CharField()
    tk_paid_time = DateTimeField()
    pub_share_fee = DecimalField()
    pub_share_rate = DecimalField()
    item_platform_type_text = CharField()
    refund_tag = CharField()
    subsidy_rate = DecimalField()
    tk_total_rate = DecimalField()
    seller_nick = CharField()
    pub_id = CharField()
    alimama_rate = DecimalField()
    subsidy_type = CharField()
    pub_share_pre_fee = DecimalField()
    alipay_total_price = DecimalField()
    item_title = CharField()
    site_name = CharField()
    item_num = CharField()
    subsidy_fee = DecimalField()
    tk_biz_tag = CharField()
    alimama_share_fee = DecimalField()
    trade_parent_id = CharField()
    order_type = CharField()
    tk_create_time = DateTimeField()
    flow_source = CharField()
    terminal_type = CharField()
    click_time = DateTimeField()
    tk_status = CharField()
    item_price = DecimalField()
    item_id = CharField()
    adzone_name = CharField()
    total_commission_rate = DecimalField()
    item_link = CharField()
    site_id = CharField()
    seller_shop_title = CharField()
    income_rate = DecimalField()
    total_commission_fee = DecimalField()
    tk_order_role = CharField()
    robot_bonus = DecimalField()
    user_bonus = DecimalField()
    state = CharField()  # paid, recv, check

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

