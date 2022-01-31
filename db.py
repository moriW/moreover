#! /usr/bin/env python
#
#
# @file: web
# @time: 2022/01/28
# @author: Mori
#


# import tornado.web
# import tornado.ioloop
# import tornado.httpserver
# from tornado.options import options

# # options.parse_config_file("project.conf")
# options.define("HOST", default="0.0.0.0", help="running host")
# options.define("PORT", default=8888, help="running host")
# options.define("DEBUG", default=True, help="running host")


# HANDLERS = []
# MAIN_APP = tornado.web.Application(
#     handlers=HANDLERS, default_host=options.HOST, gzip=True, debug=options.DEBUG
# )

# if __name__ == "__main__":
#     ioloop = tornado.ioloop.IOLoop.current()
#     http_server = tornado.httpserver.HTTPServer(MAIN_APP)
#     http_server.listen(options.PORT)
#     ioloop.start()

