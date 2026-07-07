
import os
import re
from pathlib import Path
from flask import Blueprint
from flask.views import View


class WebUi(Blueprint):
    """A Web User Interface for a module or domain.
    
    This is a extended Flask Blueprint whose name and url_prefix are automatically generated.
    It is automatically detected during app loading. It is required for web routing.

    Parameters:
        location: The filepath of related views

    """

    def __init__(self, location):
        # split path components
        path_components = []
        current_file = location
        while current_file != os.path.dirname(current_file):
            path_components.append(os.path.basename(current_file))
            current_file = os.path.dirname(current_file)
        path_components.append(current_file)
        path_components.reverse()

        # search root name
        i = path_components.index('views.py')
        root_name = path_components[i-1]

        # search import name
        j = path_components.index('modules')
        import_parts = path_components[j:]
        import_parts[-1] = import_parts[-1].replace(".py", "")
        import_name = ".".join(import_parts)

        # calcul url_prefix
        url_prefix = '/'
        if root_name not in ['home', 'auth']:
            url_prefix += root_name

        # search static url
        static_url_path = os.path.join(*path_components[:i])
        static_url_path = os.path.join(static_url_path, 'assets')
        super().__init__(root_name, 
                         import_name, 
                         url_prefix=url_prefix,
                         template_folder='pages', 
                         static_folder=static_url_path,
                         static_url_path=static_url_path)
        

    def route(self, rule, **options):
        def decorator(cls):
            if hasattr(cls, 'methods'):
                methods = cls.methods
            else:
                methods = [
                    name.upper()
                    for name in ("get", "post", "put", "patch", "delete")
                    if hasattr(cls, name)
                ]

            self.add_url_rule(
                rule,
                cls.__name__.lower(),
                cls.as_view(cls.__name__.lower()),
                methods=methods
            )
            return cls
        return decorator
    

class FileBasedView(View):
    """ A File-based routing engine for module frontend

    This is python object which implement file-based routing for a module Ui.
    """

    @classmethod
    def scan(cls, location):
        routes = {}
        template_dir = Path(location)
        for file in sorted(template_dir.rglob("*.html")):
            template = file.relative_to(template_dir).as_posix()
            route = cls._template_to_route(template)
            routes[route] = template
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


