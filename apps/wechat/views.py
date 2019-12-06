import traceback
import hashlib

from flask import request, current_app, make_response, jsonify

from . import wechat
from .utils import ReplyMessage
from .handlers import dispatch
from .models import db


@wechat.route("/index")
def index():

    return "test route!"


@wechat.route("/message", methods=["GET", "POST"])
def message():
    # 接入验证
    if request.method == "GET":
        s = request.args.get("signature")
        t = request.args.get("timestamp")
        n = request.args.get("nonce")
        e = request.args.get("echostr")

        token = current_app.config.get("WECHAT_TOKEN")
        data = [token, t, n]
        data.sort()

        temp= "".join(data).encode("utf-8")

        ms = hashlib.sha1(temp).hexdigest()

        if ms==s:
            return e
    # 消息处理
    else:
        reply = ReplyMessage(request)
        try:
            handler = dispatch(db, reply.receiveContent, openId=reply.fromWho)
            handler.save_message()

            reply.text = handler.get_message()
        except Exception as e:
            current_app.logger.error(traceback.format_exc())
            db.session.rollback()
            reply.text = "服务器故障"

        response = make_response(reply.text)
        response.content_type = 'application/xml'

        return response
