
import os
import re
import inspect
import importlib
from functools import partial
from pathlib import Path

from flask import Blueprint, render_template
from flask_restx import Namespace


class Ui(Blueprint):
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
        if rule.endswith('/'):
            rule = rule[:-1]
        return '/' + rule
        
    
    # def scan(self):
    #     file_based_view = FileBasedView(self.location)
    #     print('\ncheck')
    #     file_based_view.scan()
    #     view_func = file_based_view.as_view("solve")
    #     for url in file_based_view.routes:
    #         print('\n\tadd rule', url)
    #         self.add_url_rule(url, view_func=view_func)
    #     self.file_based_view = file_based_view

    
class ModuleApi(Namespace):

    def __init__(self, import_file):
        # split path components
        path_components = []
        current_file = import_file
        while current_file != os.path.dirname(current_file):
            path_components.append(os.path.basename(current_file))
            current_file = os.path.dirname(current_file)
        path_components.append(current_file)
        path_components.reverse()

        # search root name
        i = path_components.index('routes.py')
        root_name = path_components[i-1]

        # search api path
        base_name, version = root_name.split('_v')
        super().__init__(root_name, path=f'/{base_name}/v{version}')

    def model(self, name, *args, **kwargs):
        args = list(args)
        args.insert(0, f'{self.name}.{name}')
        return super().model(*args, **kwargs)