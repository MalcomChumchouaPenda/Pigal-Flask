
import os
import re
import inspect
import importlib
from functools import partial
from pathlib import Path

from flask import Blueprint, render_template
from flask_restx import Namespace


class ModuleUi(Blueprint):
    """A Web User Interface for a module or domain.
    
    This is a extended Flask Blueprint whose name and url_prefix are automatically generated.
    It is automatically detected during app loading. It is required for web routing.

    Parameters:
        import_name: import_name of views.py

    """

    def __init__(self, import_name):
        name = self._generate_name(import_name)
        static_dir = self._generate_static_dir(import_name)
        self.deferred_rules = []
        super().__init__(
            name, 
            import_name,
            static_folder=static_dir,
            static_url_path='../static',
            template_folder='../pages'
        )
        
    def _generate_name(self, import_name):
        names = re.findall(r'modules\.(\S+)\.pages', import_name)
        return names[0]
    
    def _generate_static_dir(self, import_name):
        spec = importlib.util.find_spec(import_name)
        if spec and spec.origin:
            routes_path = spec.origin
            pages_dir = os.path.dirname(routes_path)
            root_dir = os.path.dirname(pages_dir)
            return os.path.join(root_dir, 'static')


    def route(self, rule, **options):
        def decorator(wrapped):
            if inspect.isclass(wrapped):
                self._wrap_view_cls(wrapped, rule, options)
            else:
                self._wrap_view_func(wrapped, rule, options)
            self.deferred_rules.append(rule)
            return wrapped
        return decorator

    def _wrap_view_cls(self, view_cls, rule, options):
        view_func = view_cls.as_view(view_cls.__name__)
        self.add_url_rule(rule, view_func=view_func, **options)

    def _wrap_view_func(self, view_func, rule, options):
        self.add_url_rule(rule, view_func=view_func, **options)

    
    def scan_pages(self):
        root_dir = os.path.dirname(self.static_folder)
        pages_dir = Path(os.path.join(root_dir, 'pages'))
        for file in sorted(pages_dir.rglob("*.html")):
            template = file.relative_to(pages_dir).as_posix()
            rule = self._template_to_rule(template)
            if rule not in self.deferred_rules:
                view_func = partial(self.show_page, template)
                self.add_url_rule(rule, 'show_page', view_func,
                                  strict_slashes=False)

        
    def show_page(self, page, **kwargs):
        return render_template(page, **kwargs)
            
    
    def _template_to_rule(self, template):
        rule = re.sub(f'^{self.name}/', "", template)
        rule = re.sub(r"index\.html", "", rule)
        rule = re.sub(r"\.html", "", rule)
        rule = re.sub(
            r"\[([a-zA-Z_][a-zA-Z0-9_]*)\]",
            r"<\1>",
            rule,
        )
        rule = re.sub(r"home", "", rule)
        if rule.endswith('/'):
            rule = rule[:-1]
        if not rule.startswith('/'):
            rule = '/' + rule
        return rule

    
class ModuleApi(Namespace):

    def __init__(self, import_name):
        name = re.findall(r'\.([A-Za-z0-9_]+_v\d+)$', import_name)[0]
        super().__init__(name, description=f'{name} service')
        self.import_name = import_name

    def model(self, name, *args, **kwargs):
        args = list(args)
        args.insert(0, f'{self.name}.{name}')
        return super().model(*args, **kwargs)
    
