import requests


class MyRequest(object):

    BASE_URL = "http://121.40.164.201/wechat/statement"

    def get_sales_num(self):
        """
        获取消费详情
        """
        try:
            res = requests.get(url=MyRequest.BASE_URL)
        except Exception as e:
            print(e)
            return
        else:
            return res.json().get("data")
