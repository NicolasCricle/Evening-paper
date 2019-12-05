import logging
import platform
from flask import Flask

from configs import Config, configMap


def create_app(configName):
    """app工厂"""
    app = Flask(__name__)

    app.config.from_object(configMap[configName])
    
    from .wechat import wechat
    app.register_blueprint(wechat, url_prefix='/wechat')

    from .gitpull import git
    app.register_blueprint(git)

    cerate_logger(app)

    from apps.wechat.models import db
    db.init_app(app)

    return app


def cerate_logger(app):
    if platform.platform().startswith("Windows"):
        path = "web.log"
    else:
        path = "/var/log/web/web.log"
    fileHandler = logging.FileHandler(path)
    fileHandler.setLevel(logging.DEBUG)
    logFormat = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - line: %(lineno)s \n%(message)s')
    fileHandler.setFormatter(logFormat)

    app.logger.addHandler(fileHandler)