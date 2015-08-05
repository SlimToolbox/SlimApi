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

from tornado import gen

from ..utils.handlers import APIHandler


class BaseHandler(APIHandler):
    attrs = ['']

    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        self.collection = self.settings['db']['ota']

    @gen.coroutine
    def get_device(self, device, bail=True, create=True):
        document = yield self.collection.find_one({'device': device})
        if not document:
            if bail:
                self.fail(400, 'Unknown Device.', 1234)
            if create:
                document = {'device': device}
        return document

    @gen.coroutine
    def get_device_attrs(self, device, attrs, bail=True):
        document = yield self.get_device(device)
        if not document:
            return
        vals = []
        for attr in attrs:
            val = document.get(attr)
            if bail and not val:
                self.fail(404, '%s not set for Device' % attr, 1234)
            vals.append((attr, val))
        return vals

    @gen.coroutine
    def update_device_attrs(self, device, attrs, vals=None, create=True):
        vals = vals or []
        if not vals:
            for attr in attrs:
                val = self.get_argument_or_bail(attr)
                vals.append(val)
        document = yield self.get_device(device, bail=False)
        for i in range(len(attrs)):
            attr = attrs[i]
            val = vals[i]
            if not create and attr in document:
                self.fail(400, 'Device already has a %s.' % attr, 1234)
            document[attr] = val
        yield self.collection.save(document)

    @gen.coroutine
    def get(self, device):
        vals = yield self.get_device_attrs(device, self.attrs)
        self.success(dict(vals))

    @gen.coroutine
    def post(self, device):
        yield self.update_device_attrs(device, self.attrs, create=False)
        self.success('%s added successfully.' % ', '.join(self.attrs))

    @gen.coroutine
    def put(self, device):
        yield self.update_device_attrs(device, self.attrs)
        self.success('%s updated successfully.' % ', '.join(self.attrs))


class VersionHandler(BaseHandler):
    """Get the latest version for a device."""
    attrs = ['version']


class UrlHandler(BaseHandler):
    """Get the url of the OTA for a device."""
    attrs = ['url']


class DeviceHandler(APIHandler):

    @gen.coroutine
    def get(self, device):
        pass


app_router = [
    (r'version/(?P<device>[a-zA-Z0-9_]+)/?$', VersionHandler),
    (r'url/(?P<device>[a-zA-Z0-9_]+)/?$', UrlHandler)
]
