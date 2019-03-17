import requests
from requests_toolbelt import SSLAdapter
import pymysql


class Probe:
    def __init__(self, name, interval=10, threshold=3):
        self.name = name
        self.interval = interval
        self.warning = False
        self.warning_msg = None
        self.warning_counter = 0
        self.threshold = threshold
        self.warning_msg_tpl = self.name + "预警：%s"

    def test(self):
        print(self.name + " testing")
        self.do_test()
        self.warning = self.warning_counter >= self.threshold
        if self.warning:
            print(self.name + " has warning:" + self.warning_msg)

    def do_test(self):
        raise NotImplementedError

    def consume_warning(self):
        warning_msg = self.warning_msg
        self.warning = False
        self.warning_msg = None
        self.warning_counter = 0
        return warning_msg


class UrlProbe(Probe):
    def __init__(self, name, interval, threshold):
        super().__init__(name, interval, threshold)
        adapter = SSLAdapter('TLSv1')
        self.session = requests.Session()
        self.session.mount('https://', adapter)

    def do_test(self):
        try:
            self.session.get(self.url, timeout=10)
        except BaseException as e:
            self.warning_counter = self.warning_counter + 1
            self.warning_msg = self.warning_msg_tpl % str(e)
            print(self.warning_msg)


class SqlProbe(Probe):
    def __init__(self, name, interval, threshold):
        super().__init__(name, interval, threshold)
        db = pymysql.connect(host='localhost', user='root',
                             passwd='xxx', db='demo', port=3306, charset='utf8',
                             autocommit=True)
        self.cursor = db.cursor()

    def do_test(self):
        try:
            self.cursor.execute(self.sql)
            result = self.cursor.fetchone()
            if result[0] >= self.biz_threshold:
                self.warning_counter = self.warning_counter + 1
                self.warning_msg = self.warning_msg_tpl % (self.biz_tpl % (result[0], self.biz_threshold))
                print(self.warning_msg)
        except BaseException as e:
            self.warning_counter = self.warning_counter + 1
            self.warning_msg = self.warning_msg_tpl % str(e)
            print(self.warning_msg)
