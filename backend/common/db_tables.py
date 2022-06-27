from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Text, Boolean, Float, TIMESTAMP
from datetime import datetime

import db_conf

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_conf.DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# db = SQLAlchemy(app, session_options={'autocommit':True})
db = SQLAlchemy(app)


class TokenProfile_usdc(db.Model):
    __tablename__ = 'TokenProfile_usdc'
    id = db.Column('id', Integer, primary_key=True)
    address = db.Column('address', String(40))
    amount = db.Column('amount', String(64))
    amount_uds = db.Column('amount_uds', String(64))
    balance = db.Column('balance', String(64))
    app.config['SQLALCHEMY_DATABASE_URI'] = db_conf.DB_URI



class GasPrice(db.Model):
    """Documentation for GasPrice

    """
    __tablename__ = 'GasPrice'
    id = db.Column('id', Integer, primary_key=True)
    block_height = db.Column('block_height', String(64))
    gas_price = db.Column('gas_price', Integer)


class TransferLogs(db.Model):
    __tablename__ = 'TransferLogs'
    id = db.Column('id', Integer, primary_key=True)
    from_address = db.Column('from_address', String(40))
    to_address = db.Column('to_address', String(40))
    hash = db.Column('hash', String(64))
    cff_amount = db.Column('cff_amount', String(64))
    pub_date = db.Column('pub_date', Integer)


class UserLogs(db.Model):
    __tablename__ = 'UserLogs'
    id = db.Column('id', Integer, primary_key=True)
    address = db.Column('address', String(40))
    hash = db.Column('hash', String(64))
    usdc_amount = db.Column('usdc_amount', String(64))
    cff_amount = db.Column('cff_amount', String(64))
    usdc_fee = db.Column('usdc_fee', String(64))
    virtual_price = db.Column('virtual_price', String(64))
    operation_type = db.Column('type', String(64))

    pub_date = db.Column('pub_date', Integer)


class PriceLogs(db.Model):
    __tablename__ = 'PriceLogs'
    id = db.Column('id', Integer, primary_key=True)
    cff_amount = db.Column('cff_amount_total', String(64))
    virtual_price = db.Column('virtual_price', String(64))

    pub_date = db.Column('pub_date', Integer)


class PriceHistory(db.Model):
    __tablename__ = 'PriceHistory'
    id = db.Column('id', Integer, primary_key=True)
    cff_amount = db.Column('cff_amount_total', String(64))
    virtual_price = db.Column('virtual_price', String(64))

    pub_date = db.Column('pub_date', Integer)


class ProfitLogs(db.Model):
    __tablename__ = 'ProfitLogs'
    id = db.Column('id', Integer, primary_key=True)
    profit_usdc = db.Column('profit_usdc', String(64))
    profit_ratio = db.Column('profit_ratio', Float)
    pub_date = db.Column('pub_date',
                         TIMESTAMP(timezone=False),
                         nullable=False,
                         default=datetime.now())
    pub_date = db.Column('pub_date', Integer)

class TokenProfile_wbtc(db.Model):
    __tablename__ = 'TokenProfile_wbtc'
    id = db.Column('id', Integer, primary_key=True)
    address = db.Column('address', String(40))
    amount = db.Column('amount', String(64))


class TransferLogsWbtc(db.Model):
    __tablename__ = 'TransferLogsWbtc'
    id = db.Column('id', Integer, primary_key=True)
    from_address = db.Column('from_address', String(40))
    to_address = db.Column('to_address', String(40))
    hash = db.Column('hash', String(64))
    cff_amount = db.Column('cff_amount', String(64))

    pub_date = db.Column('pub_date', Integer)


class UserLogsWbtc(db.Model):
    __tablename__ = 'UserLogsWbtc'
    id = db.Column('id', Integer, primary_key=True)
    address = db.Column('address', String(40))
    hash = db.Column('hash', String(64))
    usdc_amount = db.Column('usdc_amount', String(64))
    cff_amount = db.Column('cff_amount', String(64))
    usdc_fee = db.Column('usdc_fee', String(64))
    virtual_price = db.Column('virtual_price', String(64))
    operation_type = db.Column('type', String(64))

    pub_date = db.Column('pub_date', Integer)


class PriceLogsWbtc(db.Model):
    __tablename__ = 'PriceLogsWbtc'
    id = db.Column('id', Integer, primary_key=True)
    cff_amount = db.Column('cff_amount_total', String(64))
    virtual_price = db.Column('virtual_price', String(64))

    pub_date = db.Column('pub_date', Integer)


class PriceHistoryWbtc(db.Model):
    __tablename__ = 'PriceHistoryWbtc'
    id = db.Column('id', Integer, primary_key=True)
    cff_amount = db.Column('cff_amount_total', String(64))
    virtual_price = db.Column('virtual_price', String(64))

    pub_date = db.Column('pub_date', Integer)


class ProfitLogsWbtc(db.Model):
    __tablename__ = 'ProfitLogsWbtc'
    id = db.Column('id', Integer, primary_key=True)
    profit_usdc = db.Column('profit_usdc', String(64))
    profit_ratio = db.Column('profit_ratio', Float)

    pub_date = db.Column('pub_date', Integer)



class TokenProfile_eth(db.Model):
    __tablename__ = 'TokenProfile_eth'
    id = db.Column('id', Integer, primary_key=True)
    address = db.Column('address', String(40))
    amount = db.Column('amount', String(64))


class TransferLogsEth(db.Model):
    __tablename__ = 'TransferLogsEth'
    id = db.Column('id', Integer, primary_key=True)
    from_address = db.Column('from_address', String(40))
    to_address = db.Column('to_address', String(40))
    hash = db.Column('hash', String(64))
    cff_amount = db.Column('cff_amount', String(64))

    pub_date = db.Column('pub_date', Integer)


class UserLogsEth(db.Model):
    __tablename__ = 'UserLogsEth'
    id = db.Column('id', Integer, primary_key=True)
    address = db.Column('address', String(40))
    hash = db.Column('hash', String(64))
    usdc_amount = db.Column('usdc_amount', String(64))
    cff_amount = db.Column('cff_amount', String(64))
    usdc_fee = db.Column('usdc_fee', String(64))
    virtual_price = db.Column('virtual_price', String(64))
    operation_type = db.Column('type', String(64))

    pub_date = db.Column('pub_date', Integer)


class PriceLogsEth(db.Model):
    __tablename__ = 'PriceLogsEth'
    id = db.Column('id', Integer, primary_key=True)
    cff_amount = db.Column('cff_amount_total', String(64))
    virtual_price = db.Column('virtual_price', String(64))

    pub_date = db.Column('pub_date', Integer)


class PriceHistoryEth(db.Model):
    __tablename__ = 'PriceHistoryEth'
    id = db.Column('id', Integer, primary_key=True)
    cff_amount = db.Column('cff_amount_total', String(64))
    virtual_price = db.Column('virtual_price', String(64))

    pub_date = db.Column('pub_date', Integer)


class ProfitLogsEth(db.Model):
    __tablename__ = 'ProfitLogsEth'
    id = db.Column('id', Integer, primary_key=True)
    profit_usdc = db.Column('profit_usdc', String(64))
    profit_ratio = db.Column('profit_ratio', Float)

    pub_date = db.Column('pub_date', Integer)


if __name__ == '__main__':
    db.create_all()
