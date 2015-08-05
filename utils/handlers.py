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

from tornado.web import RequestHandler, Finish, MissingArgumentError
from .encoders import SUPPORTED_ENCODERS


class APIHandler(RequestHandler):

    def _encoder_factory(self):
        fmt = self.get_argument('format', None)
        if fmt is None:
            fmt = self.request.headers.get('Accept', 'json').lower()
        fmt = fmt.split('/')[-1].lstrip('x-')
        if fmt not in SUPPORTED_ENCODERS:
            fmt = 'json'
        return SUPPORTED_ENCODERS.get(fmt)

    def write(self, chunk):
        if self._finished:
            raise RuntimeError("Cannot write() after finish()")

        if isinstance(chunk, dict):
            encoder = self._encoder_factory()
            pretty = self.get_argument('pretty', False) in ('true', 'y', '1', 'pretty')
            chunk = encoder['encoder'](chunk, pretty=pretty)
            for header in encoder.get('headers', ()):
                self.set_header(header[0], header[1])
        super().write(chunk)

    def get_argument_or_bail(self, attr):
        try:
            return self.get_argument(attr)
        except MissingArgumentError:
            self.fail(400, 'Missing %s parameter.' % attr, 1234)

    def success(self, data, bail=True):
        self.finish({
            'status': 'success',
            'data': data
        })
        if bail:
            raise Finish()

    def fail(self, status_code, data, code=None, bail=True):
        self.set_status(status_code)
        self.finish(chunk={
            'status': 'fail',
            'code': code or status_code,
            'data': data,
        })
        if bail:
            raise Finish()

    def error(self, status_code, message, data=None, code=None, bail=True):
        self.set_status(status_code)
        self.finish(chunk={
            'status': 'error',
            'code': code or status_code,
            'message': message,
            'data': data
        })
        if bail:
            raise Finish()
