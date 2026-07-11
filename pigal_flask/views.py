
import os
import re
from pathlib import Path
from flask import Blueprint
from flask.views import View
    

class FileBasedView(View):
    """ A File-based routing engine for module frontend

    This is python object which implement file-based routing for a module ModuleUi.
    """

    def __init__(self, location):
        super().__init__()
        self.location = location
        self.routes = {}

    def scan(self):
        routes = {}
        dirname = os.path.dirname(self.location)
        pagesdir = os.path.join(dirname, 'pages')
        template_dir = Path(pagesdir)
        for file in sorted(template_dir.rglob("*.html")):
            print('\ntchecking', file)
            template = file.relative_to(template_dir).as_posix()
            route = self._template_to_route(template)
            routes[route] = template
        self.routes = routes
        return routes
    
    @classmethod
    def _template_to_route(cls, template):
        route = re.sub(r"index\.html", "", template)
        route = re.sub(r"\.html", "", route)
        route = re.sub(
            r"\[([a-zA-Z_][a-zA-Z0-9_]*)\]",
            r"<\1>",
            route,
        )
        if route.endswith('/'):
            route = route[:-1]
        return '/' + route


