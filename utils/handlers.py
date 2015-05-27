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

from tornado.web import RequestHandler


class JsonHandler(RequestHandler):

    def success(self, data):
        self.finish({
            'status': 'success',
            'data': data
        })

    def fail(self, status_code, data, code=None):
        self.set_status(status_code)
        self.finish(chunk={
            'status': 'fail',
            'code': code or status_code,
            'data': data,
        })

    def error(self, status_code, message, data=None, code=None):
        self.set_status(status_code)
        self.finish(chunk={
            'status': 'error',
            'code': code or status_code,
            'message': message,
            'data': data
        })