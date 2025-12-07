
import os
import re
import sys
import inspect
from importlib import import_module
from flask import Blueprint
from flask_restx import Api
# from flask_sqlalchemy import SQLAlchemy
# from .utils import bind_key, tablename
from . import utils


_SERVICE_PATTERN = '^([a-z][a-z0-9_]*)_(v[0-9]+)$'


class InvalidProjectStructure(Exception):
    pass

class InvalidProjectConfig(Exception):
    pass


class Pigal:

    def __init__(self, app=None):
        super().__init__()
        self.api = None
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initializes the Flask app"""
        self._check_project_structure(app)
        self._check_project_config(app)
        self._setup_api(app)
        self._register_pages(app)
        self._register_services(app)


    def _check_project_structure(self, app):
        project_dir = os.path.dirname(app.instance_path)
        for required_name in ('app', 'pages', 'services'):
            required_dir = os.path.join(project_dir, required_name)
            if not os.path.isdir(required_dir):
                msg = f"'{required_name}' directory is required but not found"
                raise InvalidProjectStructure(msg)
    
    def _check_project_config(self, app):
        for name in ('PIGAL_PROJECT_NAME', 'PIGAL_PROJECT_VERSION'):
            if name not in app.config:
                msg = f"Configuration parameter '{name}' is missing"
                raise InvalidProjectConfig(msg)

    def _setup_api(self, app):
        config = app.config
        title = config['PIGAL_PROJECT_NAME'] + ' API'
        version = config['PIGAL_PROJECT_VERSION']
        api_bp = Blueprint('api', __name__, url_prefix='/api')
        api = Api(api_bp, title=title, version=version)
        app.register_blueprint(api_bp)
        self.api = api

        
    def _register_pages(self, app):
        app.logger.debug('looking for pages...')
        project_dir = os.path.dirname(app.instance_path)
        pages_dir = os.path.join(project_dir, 'pages')
        if os.path.isdir(pages_dir):
            for name in os.listdir(pages_dir):
                if name.startswith('_'):
                    continue 
                url_prefix = f'/{name}' 
                ui_root = f'pages.{name}'
                self._register_page(app, ui_root, url_prefix)
                
    def _register_page(self, app, ui_root, url_prefix):
        try:
            routes = import_module(f'{ui_root}.routes')
            ui = routes.ui
        except (ModuleNotFoundError, AttributeError) as e:
            app.logger.warning(e)
            return False
        
        if not isinstance(ui, utils.PigalUi):
            name = url_prefix[1:]
            msg = f"The object 'ui' of page '{name}' "
            msg += "is not an instance of 'PigalUi'"
            raise utils.InvalidPageUi(msg)
        
        # menus = import_module(f'{ui_root}.menus')
        app.register_blueprint(routes.ui, url_prefix=url_prefix)
        app.logger.info(f'Register page: {ui_root} => {url_prefix}')
        return True


    def _register_services(self, app):
        app.logger.debug('looking for services...')
        project_dir = os.path.dirname(app.instance_path)
        services_dir = os.path.join(project_dir, 'services')
        if os.path.isdir(services_dir):
            for name in os.listdir(services_dir):
                if name.startswith('_'):
                    continue
                # nameparts = re.findall(_SERVICE_PATTERN, name)
                # if len(nameparts) != 1:
                #     app.logger.warning('Ignore folder: '+ name)
                #     continue
                # rootname, version = nameparts[0]
                # rootname = rootname.replace('_', '-')
                # version = version.replace('_', '.')
                # url_prefix = f'/{rootname}/{version}'
                # url_prefix = '/test'
                service_root = f'services.{name}'
                self._register_service(app, service_root)

    def _register_service(self, app, service_root):
        try:
            routes = import_module(f'{service_root}.routes')
            print(routes.api)
            self.api.add_namespace(routes.api)
            url_prefix = routes.api.path
            app.logger.info(f'Register service: {service_root} => {url_prefix}')
            return True
        except (ModuleNotFoundError, AttributeError) as e:
            app.logger.warning(e)

# class PigalDb(SQLAlchemy):
#     """The Extended Db for Pigal Projects backend"""

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         setattr(self.Model, '__tablename__', tablename)
#         setattr(self.Model, '__bind_key__', bind_key)

#     def init_app(self, app):
#         self._prepare_db(app)
#         return super().init_app(app)
    
    
#     @classmethod
#     def _minify_uri(cls, uri):
#         if len(uri) > 50:
#             return uri[:20] + '...' + uri[-20:]
#         return uri
    
#     def _prepare_db(self, app):
#         app.logger.debug('looking for databases...')
#         root_dir = os.path.abspath(app.config['PIGAL_ROOT_DIR'])
#         uri_template = app.config['PIGAL_DB_URI_TEMPLATE']
#         uri_args = {'root_dir':root_dir}

#         # by default
#         uri_args['service_id'] = 'default'
#         uri = uri_template.format_map(uri_args)
#         min_uri = self._minify_uri(uri)
#         app.config['SQLALCHEMY_DATABASE_URI'] = uri
#         app.logger.debug(f'Prepare database: default => {min_uri}')

#         # by services
#         services_dir = os.path.join(root_dir, 'services')
#         bind_keys = {}
#         if os.path.isdir(services_dir):
#             for name in os.listdir(services_dir):
#                 # check if has models
#                 if name.startswith('_'):
#                     continue
#                 if not re.match(_SERVICE_PATTERN, name):
#                     continue
#                 modelspath = os.path.join(services_dir, name, 'models.py')
#                 if not os.path.isfile(modelspath):
#                     continue
#                 _ = import_module(f'services.{name}.models') # important to load metada

#                 # create binds for sqlalchemy
#                 uri_args['service_id'] = name
#                 uri = uri_template.format_map(uri_args)
#                 min_uri = self._minify_uri(uri)
#                 bind_keys[name] = uri
#                 app.logger.debug(f'Prepare database: {name} => {min_uri}')
        
#         # store models binds
#         app.config['SQLALCHEMY_BINDS'] = bind_keys

