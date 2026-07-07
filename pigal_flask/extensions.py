
import os
import re
import sys
import inspect
import warnings
from importlib import import_module

from flask import Blueprint
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SAWarning

from . import utils
from . import views
from . import exceptions as exc


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
        self._register_frontends(app)
        self._register_backends(app)


    def _check_project_structure(self, app):
        project_dir = os.path.dirname(app.instance_path)
        for required_name in ('app', 'modules'):
            required_dir = os.path.join(project_dir, required_name)
            if not os.path.isdir(required_dir):
                msg = f"'{required_name}' directory is required but not found"
                raise exc.InvalidProjectStructure(msg)
    
    def _check_project_config(self, app):
        for name in ('PIGAL_PROJECT_NAME', 'PIGAL_PROJECT_VERSION'):
            if name not in app.config:
                msg = f"Configuration parameter '{name}' is missing"
                raise exc.InvalidProjectConfig(msg)

    def _setup_api(self, app):
        config = app.config
        title = config['PIGAL_PROJECT_NAME'] + ' API'
        version = config['PIGAL_PROJECT_VERSION']
        api_bp = Blueprint('api', __name__, url_prefix='/api')
        api = Api(api_bp, title=title, version=version)
        app.register_blueprint(api_bp)
        self.api = api

        
    def _register_frontends(self, app):
        app.logger.debug('looking for frontends...')
        project_dir = os.path.dirname(app.instance_path)
        frontends_dir = os.path.join(project_dir, 'modules')
        if os.path.isdir(frontends_dir):
            for name in os.listdir(frontends_dir):
                if name.startswith('_'):
                    continue 
                url_prefix = f'/{name}' 
                ui_root = f'modules.{name}'
                self._register_frontend(app, ui_root, url_prefix)
                
    def _register_frontend(self, app, ui_root, url_prefix):
        try:
            routes = import_module(f'{ui_root}.views')
            ui = routes.ui
        except (ModuleNotFoundError, AttributeError) as e:
            app.logger.warning(e)
            return False
        
        if not isinstance(ui, views.WebUi):
            name = url_prefix[1:]
            msg = f"The object 'ui' of module '{name}' "
            msg += "is not an instance of 'WebUi'"
            raise exc.InvalidUi(msg)
        
        # menus = import_module(f'{ui_root}.menus')
        app.register_blueprint(routes.ui, url_prefix=url_prefix)
        app.logger.info(f'Register frontend: {ui_root} => {url_prefix}')
        return True


    def _register_backends(self, app):
        app.logger.debug('looking for backends...')
        project_dir = os.path.dirname(app.instance_path)
        backends_dir = os.path.join(project_dir, 'modules')
        if os.path.isdir(backends_dir):
            for name in os.listdir(backends_dir):
                if name.startswith('_'):
                    continue
                backend_root = f'modules.{name}'
                self._register_backend(app, backend_root)

    def _register_backend(self, app, backend_root):
        try:
            routes = import_module(f'{backend_root}.routes')
            api = routes.api
        except (ModuleNotFoundError, AttributeError) as e:
            app.logger.warning(e)
            return False

        if not isinstance(api, utils.PigalApi):
            _ , name = backend_root.split('.')
            msg = f"The object 'api' of backend '{name}' "
            msg += "is not an instance of 'PigalApi'"
            raise exc.InvalidApi(msg)
        
        self.api.add_namespace(api)
        app.logger.info(f'Register backend: {backend_root} => {api.path}')
        return True

warnings.filterwarnings(
    'ignore',                            # Action: Ignore the warning
    category=SAWarning,                  # Category of the warning
    message=".*bind_key.*",              # Message pattern to match
    module="flask_sqlalchemy"            # Only suppress from this specific module
)

class PigalDb(SQLAlchemy):

    def __init__(self, *args, **kwargs):
        kwargs['disable_autonaming'] = True
        super().__init__(*args, **kwargs)
        setattr(self.Model, '__tablename__', utils.tablename)
        setattr(self.Model, '__bind_key__', utils.bind_key)

    def init_app(self, app):
        self._check_db_config(app)
        self._prepare_db(app)
        super().init_app(app)

    def _check_db_config(self, app):
        for name in ('PIGAL_DB_URI_TEMPLATE', ):
            if name not in app.config:
                msg = f"Configuration parameter '{name}' is missing"
                raise exc.InvalidProjectConfig(msg)

    @classmethod
    def _minify_uri(cls, uri):
        if len(uri) > 50:
            return uri[:20] + '...' + uri[-20:]
        return uri

    def _prepare_db(self, app):
        app.logger.debug('looking for databases...')
        project_dir = os.path.dirname(app.instance_path)
        uri_template = app.config['PIGAL_DB_URI_TEMPLATE']
        uri_args = {'project_dir':project_dir}

        # by default
        uri_args['backend_id'] = 'default'
        uri = uri_template.format_map(uri_args)
        min_uri = self._minify_uri(uri)
        app.config['SQLALCHEMY_DATABASE_URI'] = uri
        app.logger.debug(f'Prepare database: default => {min_uri}')

        # by backends
        backends_dir = os.path.join(project_dir, 'backends')
        bind_keys = {}
        if os.path.isdir(backends_dir):
            for name in os.listdir(backends_dir):
#                 # check if has models
                if name.startswith('_'):
                    continue
#                 if not re.match(_SERVICE_PATTERN, name):
#                     continue
                modelspath = os.path.join(backends_dir, name, 'models.py')
                if not os.path.isfile(modelspath):
                    continue
                _ = import_module(f'backends.{name}.models') # important to load metada

                # create binds for sqlalchemy
                uri_args['backend_id'] = name
                uri = uri_template.format_map(uri_args)
                min_uri = self._minify_uri(uri)
                bind_keys[name] = uri
                app.logger.debug(f'Prepare database: {name} => {min_uri}')
        
        # store models binds
        app.config['SQLALCHEMY_BINDS'] = bind_keys


# class PigalDb(SQLAlchemy):
#     """The Extended Db for Pigal Projects backend"""


#     def init_app(self, app):
#         self._prepare_db(app)
#         return super().init_app(app)
    
    
    

