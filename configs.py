class Config:
    DEBUG                           = False
    SQLALCHEMY_DATABASE_URI         = "mysql+pymysql://livis:123456@121.40.164.201:3306/wechat"
    SQLALCHEMY_TRACK_MODIFICATIONS  = False


configMap = {
    "config": Config
}