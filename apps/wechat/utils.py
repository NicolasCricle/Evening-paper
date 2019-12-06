import re
import time
import xmltodict



class WechatMessage(object):
    
    def __init__(self, request):
        self._request = request


class ReplyMessage(WechatMessage):

    def __init__(self, request):
        super().__init__(request)
        self.init_xml()
        self._xml = None

    def init_xml(self, request):
        xmlDict = xmltodict.parse(request.stream.read()).get("xml")
        self._toUser = xmlDict.get("ToUserName")
        self._fromUser = xmlDict.get("FromUserName")
        self._creatTime = xmlDict.get("CreateTime")
        self._type = xmlDict.get("MsgType")
        self._content = xmlDict.get("Content")
        self._msgId = xmlDict.get("MsgId")

    @property
    def receiveContent(self):
        return self._content

    @property
    def fromWho(self):
        return self._fromUser

    @property
    def text(self):
        return self._xml

    @text.setter
    def text(self, value):
        self._xml = f'<xml><ToUserName><![CDATA[{self._fromUser}]]></ToUserName>' \
                    f'<FromUserName><![CDATA[{self._toUser}]]></FromUserName>' \
                    f'<CreateTime>{str(int(time.time()))}</CreateTime>'

        self._xml += f'<MsgType><![CDATA[text]]></MsgType>'\
                     f'<Content><![CDATA[{value}]]></Content></xml>'


if __name__ == "__main__":
    pass