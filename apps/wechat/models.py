import datetime
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import cast


db = SQLAlchemy()


class BaseModel(db.Model):
    """
    设置字符集等一些公共属性
    """
    __abstract__ = True


class SalesRecord(BaseModel):
    """
    筛选出来的符合条件的销售记录
    """
    __tablename__ = "SalesRecord"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    saler = db.Column(db.String(20))
    saleNum = db.Column(db.Integer)
    createTime = db.Column(db.DateTime, default=datetime.datetime.now)
    date = db.Column(db.Date, default=datetime.date.today)

    messageId = db.Column(db.Integer, db.ForeignKey('ReceiveMessage.id'))

    @classmethod
    def sum_sales(cls):
        # sqlalchemy 分组查询测试 cast 映射 Decimal 字段为 Integer
        queryFields = [
            cls.saler,
            cast(func.sum(cls.saleNum), sqlalchemy.Integer).label("salesNum")
        ]
        filterFields = [
            cls.date == datetime.date.today()
        ]

        return db.session.query(*queryFields).filter(*filterFields).group_by(cls.saler).order_by("salesNum").all()


    @classmethod
    def sales_record(cls, saler):
        """ 获取当天的销售添加记录 """
        queryFields = [
            cls.saler,
            cls.saleNum,
            cls.createTime
        ]
        filterFields = [
            cls.date == datetime.date.today(),
            cls.saler == saler
        ]
        return db.session.query(*queryFields).filter(*filterFields).all()


class ReceiveMessage(BaseModel):
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


class DailyReport(BaseModel):
    """
    当天是否要发送报告
    """
    __tablename__ = "DailyReport"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, default=datetime.date.today)
    isReport = db.Column(db.Boolean)

