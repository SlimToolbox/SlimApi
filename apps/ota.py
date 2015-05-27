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

import tornado.web

from tornado import gen

from ..utils.handlers import JsonHandler


class BaseOTAHandler(JsonHandler):
    attr = ''

    def __init__(self, *args, **kwargs):
        super(BaseOTAHandler, self).__init__(*args, **kwargs)
        self.collection = self.settings['db']['ota']

    @gen.coroutine
    def get(self, device):
        document = yield self.collection.find_one({'device': device})
        if not document:
            return self.fail(400, 'Unknown Device.', 1234)
        val = document.get(self.attr)
        if not val:
            return self.fail(404, '%s not set for Device' % self.attr, 1234)
        return self.success({self.attr: val})

    @gen.coroutine
    def post(self, device):
        try:
            val = self.get_argument(self.attr)
        except tornado.web.MissingArgumentError:
            return self.fail(400, 'Missing %s parameter.' % self.attr, 1234)

        document = yield self.collection.find_one({'device': device})
        if document:
            if hasattr(document, self.attr):
                return self.fail(400, 'Device already has a %s.' % self.attr,
                                 1234)
            _id = document['_id']
            _ = yield self.collection.update({'_id': _id},
                                                  {'$set':
                                                   {self.attr: val}
                                                   })
        else:
            _ = yield self.collection.insert({'device': device,
                                                   self.attr: val})
        return self.success('%s added successfully.' % self.attr)

    @gen.coroutine
    def put(self, device):
        try:
            val = self.get_argument(self.attr)
        except tornado.web.MissingArgumentError:
            return self.fail(400, 'Missing %s parameter.' % self.attr, 1234)

        document = yield self.collection.find_one({'device': device})
        if not document:
            return self.fail(400, 'Unknown Device.', 1234)
        _id = document['_id']
        _ = yield self.collection.update({'_id': _id},
                                              {'$set': {self.attr: val}})
        return self.success('%s updated successfully.' % self.attr)


class OTAVersionHandler(BaseOTAHandler):
    """Get the latest version for a device."""
    attr = 'version'


class OTAUrlHandler(JsonHandler):
    """Get the url of the OTA for a device."""
    attr = 'url'


app_router = [
    (r'version/(?P<device>[a-zA-Z0-9_]+)/?$', OTAVersionHandler),
    (r'url/(?P<device>[a-zA-Z0-9_]+)/?$', OTAUrlHandler)
]
