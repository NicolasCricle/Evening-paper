import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


# class MyUser(db.Model):
#     __tablename__ = "MyUser"

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     openId = db.Column(db.String(50))
#     isDelete = db.Column(db.Boolean, default=False)

#     sales = db.relationship("SalesRecord",backref='user',lazy='dynamic')


class SalesRecord(db.Model):
    __tablename__ = "SalesRecord"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    saler = db.Column(db.String(20))
    saleNum = db.Column(db.Integer)
    createTime = db.Column(db.DateTime, default=datetime.datetime.now)

    # userId = db.Column(db.Integer, db.ForeignKey('MyUser.id'))
    messageId = db.Column(db.Integer, db.ForeignKey('ReceiveMessage.id'))


class ReceiveMessage(db.Model):
    __tablename__ = "ReceiveMessage"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    createTime = db.Column(db.DateTime, default=datetime.datetime.now)
    openId = db.Column(db.String(50))
    # userId = db.Column(db.Integer, db.ForeignKey('MyUser.id'))

    sales = db.relationship("SalesRecord",backref='message', uselist=False)

