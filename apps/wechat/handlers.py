import re
import datetime
from apps.wechat.models import SalesRecord, ReceiveMessage, DailyReport


class Regex(object):
    SALER_REGEX = r"^[\u4e00-\u9fa5]{2,4}$"
    SALES_NUM_REGEX = r"^[\u4e00-\u9fa5]{2,4}\s+-?\d+$"


salerRe = re.compile(Regex.SALER_REGEX)
salesNumRe = re.compile(Regex.SALES_NUM_REGEX)


def dispatch(db, content, **kwargs):
    if content == "今日":
        return StatementHandler(db, content, **kwargs)
    elif content == "发送":
        return DailyHandler(db, content, **kwargs)
    elif salerRe.match(content):
        return QueryHandler(db, content, **kwargs)
    elif salesNumRe.match(content):
        return AddSaleHandler(db, content, **kwargs)
    else:
        return ErrorHandler(db, content, **kwargs)


class BaseHandler(object):

    def __init__(self, db, content, **kwargs):
        self._db = db
        self._content = content
        if "openId" in kwargs:
            self._openId = kwargs.pop("openId")
        self._msgId = None

    def save_message(self):
        message = ReceiveMessage(content=self._content, openId=self._openId)
        self._db.session.add(message)
        self._db.session.flush()
        self._msgId = message.id

    def get_message(self):
        return "无合适处理流程"


class StatementHandler(BaseHandler):

    def get_message(self):
        sumList = SalesRecord.sum_sales()
        
        message = ""
        for item in sumList:
            item = item._asdict()
            message += f'{item.get("saler")}今天的销售额是：{item.get("salesNum")}\n'
        if not message: message = "今日暂无销售额"

        return message


class AddSaleHandler(BaseHandler):

    def get_message(self):
        name, sales = self._content.split()
        # 首先存入销售记录

        rd = SalesRecord(saler=name, saleNum=int(sales), messageId=self._msgId)
        self._db.session.add(rd)
        self._db.session.commit()

        sign = "加" if int(sales) > 0 else "减" 
        return f"操作成功\n{name} 今日销售额 {sign} {abs(int(sales))}"


class QueryHandler(BaseHandler):

    def get_message(self):
        rds = SalesRecord.sales_record(self._content)
        
        messages = ""
        for item in rds:
            item = item._asdict()
            messages += f'{item.get("saler")}\t{item.get("saleNum")}\t{item.get("createTime").time()}\n'
        if not messages: messages = f'{self._content} 今日暂无销售记录'
        
        return messages


class DailyHandler(BaseHandler):

    def get_message(self):
        dailyRd = DailyReport(date=datetime.date.today(), isReport=True)
        self._db.session.add(dailyRd)
        self._db.session.commit()
        return "今日晚报将在 10：45定时发送"


class ErrorHandler(BaseHandler):

    def get_message(self):
        return "error"



