import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    DEBUG                           = False
    SQLALCHEMY_DATABASE_URI         = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS  = False

    WECHAT_TOKEN                    = os.getenv("WECHAT_TOKEN")
    WECHAT_APPID                    = os.getenv("WECHAT_APPID")
    WECHAT_SECRET                   = os.getenv("WECHAT_SECRET")

    LOGGER_PATH                     = os.getenv("LOGGER_PATH")


configMap = {
    "config": Config
}


if __name__ == "__main__":
    pass