# Copyright (C) 2015 SlimRoms Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import sys

import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from motor import MotorClient
from tornado.options import define, options

from .utils import router

define("port", default=8888, help="run on the given port", type=int)
define("app", default='', help="run a specific app", type=str)


class Application(tornado.web.Application):
    def __init__(self, handlers=None, **settings):
        if not handlers:
            handlers = router.get_routes(__name__, __file__,
                                         app_name=options.app)
        super(Application, self).__init__(handlers, **settings)


def main(args):
    tornado.options.parse_command_line(args)
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.bind(options.port)
    http_server.start(0)
    app.settings['db'] = MotorClient()['SlimApi']
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main(sys.argv)
