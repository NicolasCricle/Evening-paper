import traceback
import hashlib

from flask import request, current_app, make_response

from . import wechat
from .utils import ReplyMessage, get_sales_num
from apps.wechat.models import MyUser, SalesRecord, ReceiveMessage, db



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

            # 检查发消息的人是否存在，不存在添加入MyUser
            user = MyUser.query.filter(openId==reply.fromWho).first()
            if not user:
                user = MyUser(openId=reply.fromWho)
                db.session.add(user)
                db.session.commit()

            data, message = get_sales_num(replay.receiveContent)
            if data:
                reply.text = f"操作成功，{data.get('name')}的 销售数额 {data.get('sales')}"
                # 数据写入数据库
                rece = ReceiveMessage(content=reply.receiveContent, userId=user.id)
                db.session.add(rece)

                sales = SalesRecord(saler=data.get("name"), saleNum=data.get("sales"), userId=user.id, messageId=rece.id)
                db.session.add(sales)

                db.session.commit()
            else:
                reply.text = message

        except Exception as e:
            current_app.logger.error(traceback.format_exc())
            db.session.rollback()

        response = make_response(reply.text)
        response.content_type = 'application/xml'

        return response
