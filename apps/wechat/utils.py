import re
import time
import xmltodict



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