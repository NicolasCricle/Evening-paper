from flask import request, current_app, make_response
from . import wechat
from .utils import ReplyMessage
import hashlib


@wechat.route("/index")
def index():
    return "hello world!!!"


@wechat.route("/message", methods=["GET", "POST"])
def message():
    # 接入验证
    if request.method == "GET":
        s = request.args.get("signature")
        t = request.args.get("timestamp")
        n = request.args.get("nonce")
        e = request.args.get("echostr")

        token = "Z470588044L"
        data = [token, t, n]
        data.sort()

        temp= "".join(data).encode("utf-8")

        ms = hashlib.sha1(temp).hexdigest()

        if ms==s:
            return e
    # 消息处理
    else:
        try:
            reply = ReplyMessage(request)
            reply.text = "您好！"
        except Exception as e:
            current_app.logger.error(str(e))

        response = make_response(reply.text)
        response.content_type = 'application/xml'

        return response
