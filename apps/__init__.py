from flask import Flask
from configs import Config, configMap


def create_app(configName):
    """app工厂"""
    app = Flask(__name__)

    app.config.from_object(configMap[configName])
    
    from .wechat import wechat
    app.register_blueprint(wechat)

    from .gitpull import git
    app.register_blueprint(git)

    return app