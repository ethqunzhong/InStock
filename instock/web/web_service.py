#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import logging
import datetime
import os.path
import sys
from abc import ABC
import tornado.escape
from tornado import gen
import tornado.httpserver
import tornado.ioloop
import tornado.options

# 在项目运行时，临时将项目路径添加到环境变量
cpath_current = os.path.dirname(os.path.dirname(__file__))
cpath = os.path.abspath(os.path.join(cpath_current, os.pardir))
sys.path.append(cpath)
log_path = os.path.join(cpath_current, 'log')
log_web_path = os.path.join(cpath_current, 'log/web')
if not os.path.exists(log_web_path):
    os.makedirs(log_web_path)

current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
log_filename = 'stock_execute_job-{}.log'.format(current_time)
logging.basicConfig(format='%(asctime)s %(message)s', filename=os.path.join(log_web_path, log_filename))

import instock.lib.torndb as torndb
import instock.lib.database as mdb
import instock.lib.version as version
import instock.web.dataTableHandler as dataTableHandler
import instock.web.dataIndicatorsHandler as dataIndicatorsHandler
import instock.web.base as webBase

__author__ = 'myh '
__date__ = '2023/3/10 '


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            # 设置路由
            (r"/", HomeHandler),
            (r"/instock/", HomeHandler),
            # 使用datatable 展示报表数据模块。
            (r"/instock/api_data", dataTableHandler.GetStockDataHandler),
            (r"/instock/data", dataTableHandler.GetStockHtmlHandler),
            # 获得股票指标数据。
            (r"/instock/data/indicators", dataIndicatorsHandler.GetDataIndicatorsHandler),
        ]
        settings = dict(  # 配置
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,  # True,
            # cookie加密
            cookie_secret="027bb1b670eddf0392cdda8709268a17b58b7",
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)
        # Have one global connection to the blog DB across all handlers
        self.db = torndb.Connection(**mdb.MYSQL_CONN_TORNDB)


# 首页handler。
class HomeHandler(webBase.BaseHandler, ABC):
    @gen.coroutine
    def get(self):
        self.render("index.html",
                    stockVersion=version.__version__,
                    leftMenu=webBase.GetLeftMenu(self.request.uri))


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    port = 9999
    http_server.listen(port)

    # tornado.options.log_file_prefix = os.path.join(cpath, '/logs/stock_web.log')
    tornado.options.options.logging = None
    # tornado.options.parse_command_line()
    logging.getLogger().setLevel(logging.INFO)

    print("服务已启动，web地址 : http://localhost:9999/")
    logging.info("服务已启动，web地址 : http://localhost:9999/")

    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
