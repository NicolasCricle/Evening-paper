from flask import request
from . import wechat
import hashlib


@wechat.route("/index")
def index():
    return "hello world!???===000"


@wechat.route("/message", methods=["GET", "POST"])
def message():
    if request.method == "GET":
        s = request.args.get("signature")
        t = request.args.get("timestimp")
        n = request.args.get("nonce")
        e = request.args.get("echostr")

        token = "Z470588044L"
        data = [token, t, n]
        data.sort()

        temp= "".join(data)

        ms = hashlib.sha1(temp).hexdigest()

        if ms==m:
            return e