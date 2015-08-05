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


SUPPORTED_ENCODERS = {}


import json


def json_encode(obj, pretty=False):
    kwargs = {}
    if pretty:
        kwargs['indent'] = 4
        kwargs['separators'] = (',', ': ')
    return json.dumps(obj, **kwargs).replace("</", "<\\/")
SUPPORTED_ENCODERS.update({
    'json': {
        'headers': (("Content-Type", "application/json; charset=UTF-8"),),
        'encoder': json_encode
    }
})


try:
    import xmltodict
except ImportError:
    pass
else:
    def xml_encode(obj, pretty=False):
        if len(obj) == 1:
            obj = {'root': obj}
        return xmltodict.unparse(obj, pretty=pretty)
    SUPPORTED_ENCODERS.update({
        'xml': {
            'headers': (("Content-Type", "application/xml; charset=UTF-8"),),
            'encoder': xml_encode
        }
    })


try:
    import yaml
except ImportError:
    pass
else:
    def yaml_encode(obj, pretty=False):
        yaml.safe_dump(obj, default_flow_style=(not pretty))
    SUPPORTED_ENCODERS.update({
        'yaml': {
            'headers': (("Content-Type", "text/yaml; charset=UTF-8"),),
            'encoder': yaml_encode
        }
    })
