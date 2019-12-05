import re
import time
import xmltodict

from apps.wechat.models import Saler, SalesRecord, ReceiveMessage, DailyReport, db


class WechatMessage(object):
    
    def __init__(self, request):
        self._request = request
        self.token = "Z470588044L"
        self.appid = "wx1eff2f2a8e61a2ea"
        self.secret = "713feb00fef3f0922d73f788f3a84b7c"
    

class ReplyMessage(WechatMessage):

    def __init__(self, request):
        super().__init__(request)
        self._xmlStr = request.stream.read()
        self.init_xml()
        self._xml = None

    def init_xml(self):
        xmlDict = xmltodict.parse(self._xmlStr).get("xml")
        self.toUser = xmlDict.get("ToUserName")
        self.fromUser = xmlDict.get("FromUserName")
        self.creatTime = xmlDict.get("CreateTime")
        self._type = xmlDict.get("MsgType")
        self.content = xmlDict.get("Content")
        self.msgId = xmlDict.get("MsgId")

    @property
    def receiveContent(self):
        return self.content

    @property
    def fromWho(self):
        return self.fromUser

    @property
    def text(self):
        return self._xml

    @text.setter
    def text(self, value):
        self._xml = f'<xml><ToUserName><![CDATA[{self.fromUser}]]></ToUserName>' \
                    f'<FromUserName><![CDATA[{self.toUser}]]></FromUserName>' \
                    f'<CreateTime>{str(int(time.time()))}</CreateTime>'

        self._xml += f'<MsgType><![CDATA[text]]></MsgType>'\
                     f'<Content><![CDATA[{value}]]></Content></xml>'


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

        sign = "加" if sales > 0 else "减" 
        return f"操作成功\n{name} 今日销售额 {sign} {abs(sales)}"


class Person(BaseRes):

    pass


class ErrorM(BaseRes):

    def get_message(self):
        return "error"



def get_sales_num(content):
    content = content.split()
    if len(content) != 2:
        return None, "销售的数据格式为：销售人  销售数额"
    try:
        salesNum = int(content[1])
    except Exception as e:
        return None, "销售数额必须是数字"
    else:
        return {"name": content[0], "salesNum": salesNum}, ""


if __name__ == "__main__":
    dispatch("今阿斯1000000")