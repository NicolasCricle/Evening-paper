import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class SalesRecord(db.Model):
    """
    筛选出来的符合条件的销售记录
    """
    __tablename__ = "SalesRecord"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    saler = db.Column(db.String(20))
    saleNum = db.Column(db.Integer)
    createTime = db.Column(db.DateTime, default=datetime.datetime.now)
    date = db.Column(db.Date, default=datetime.date.today)

    # userId = db.Column(db.Integer, db.ForeignKey('MyUser.id'))
    messageId = db.Column(db.Integer, db.ForeignKey('ReceiveMessage.id'))

    @classmethod
    def sum_sales(cls):
        rds = cls.query.filter(cls.date==datetime.date.today()).all()
        temp = dict()
        for rd in rds:
            if rd.saler in temp:
                temp[rd.saler] += rd.saleNum
            else:
                temp[rd.saler] = rd.saleNum

        sumList = [{"saler": name, "salesNum": salesNum} for name, salesNum in temp.items()]

        sorted(sumList, key=lambda x: x.get(salesNum))
        return sumList

        

class ReceiveMessage(db.Model):
    """
    接受的微信端消息记录
    """
    __tablename__ = "ReceiveMessage"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    createTime = db.Column(db.DateTime, default=datetime.datetime.now)
    openId = db.Column(db.String(50))
    # userId = db.Column(db.Integer, db.ForeignKey('MyUser.id'))

    sales = db.relationship("SalesRecord",backref='message', uselist=False)


class DailyReport(db.Model):
    """
    当天是否要发送报告
    """
    __tablename__ = "DailyReport"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, default=datetime.date.today)
    isReport = db.Column(db.Boolean)

