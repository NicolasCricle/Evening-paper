from . import wechat


@wechat.route("/index")
def index():
    return "hello world!"