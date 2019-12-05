import re
from apps.wechat.models import SalesRecord, ReceiveMessage, DailyReport, db


class Regex(object):
    SALER_REGEX = r"^[\u4e00-\u9fa5]{2,4}$"
    SALES_NUM_REGEX = r"^[\u4e00-\u9fa5]{2,4}\s+-?\d+$"


salerRe = re.compile(Regex.SALER_REGEX)
salesNumRe = re.compile(Regex.SALES_NUM_REGEX)


def dispatch(content, openId):
    if content == "今日":
        return Statement(content, openId)
    elif salerRe.match(content):
        return Person(content, openId)
    elif salesNumRe.match(content):
        return AddSalersNum(content, openId)
    else:
        return ErrorM(content, openId)


class BaseRes(object):

    def __init__(self, content, openId):
        self._content = content
        self._openId = openId
        self._msgId = None

    def save_message(self):
        message = ReceiveMessage(content=self._content, openId=self._openId)
        db.session.add(message)
        db.session.flush()
        self._msgId = message.id

    def get_message(self):
        return "OK"


class Statement(BaseRes):

    def get_message(self):
        sumList = SalesRecord.sum_sales()
        message = ""
        for item in sumList:
            message += f'{item.get("saler")}今天的销售额是：{item.get("salesNum")}\n'

        return message


class AddSalersNum(BaseRes):

    def get_message(self):
        name, sales = self._content.split()
        # 首先存入销售记录

        rd = SalesRecord(saler=name, saleNum=int(sales), messageId=self._msgId)
        db.session.add(rd)
        db.session.commit()

        sign = "加" if int(sales) > 0 else "减" 
        return f"操作成功\n{name} 今日销售额 {sign} {abs(sales)}"


class Person(BaseRes):

    pass


class ErrorM(BaseRes):

    def get_message(self):
        return "error"