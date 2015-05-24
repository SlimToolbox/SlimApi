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

import importlib.machinery
import os


def add_routes(router, app_dir=None):
    """Add all the routes within the apps director, adding the required
       base urls.

    Each python file in the apps directory is assumed to require a route
    adding. Rather than mapping each route out in one place, this will
    allow an app to have their own area, and this routine will prepend
    the apps route with a base route.

    Example:
      apps/example.py contains a request handler called simple.
      A global variable must be created, called app_router.
      To this, an iterable must be set:
        app_router = (
            ('GET', '/simple', simple),
        )
      add_routes will detect this, and create an equivilant route as:
        add_route('GET', '/example/simple', simple)


    :param router: router object from the base app
    :param app_dir: defaults to 'apps/' relative to this file
                    the directory to
    """
    app_dir = app_dir or os.path.join(os.path.dirname(
        os.path.dirname(__file__)), 'apps')
    # Don't bother checking here. let it fall through

    for py_file in os.listdir(app_dir):
        if (py_file.startswith('_') or not py_file.endswith('.py') or
                os.path.isdir(os.path.join(app_dir, py_file))):
            continue
        name = py_file[:-3]

        app = importlib.machinery.SourceFileLoader(
            name, os.path.join(app_dir, py_file)).load_module()

        if not hasattr(app, 'app_router'):
            continue

        app_router = getattr(app, 'app_router')
        for app_route in app_router:
            method = app_route[0]
            path = app_route[1].lstrip('/')
            handler = app_route[2]
            _name = app_route[3] if len(app_route) > 3 else None
            expect_handler = app_route[4] if len(app_route) > 4 else None
            path = os.path.join('/%s' % name, path)
            router.add_route(method, path, handler,
                             name=_name, expect_handler=expect_handler)
