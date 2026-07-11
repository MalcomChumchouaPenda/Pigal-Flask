
import os
import re
import sys
import inspect
import warnings
import importlib

from flask import Blueprint
from flask_restx import Api 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SAWarning

from . import utils
from . import views
from . import exceptions as exc
from ._interfaces import ModuleUi
from ._interfaces import ModuleApi


class RouteManager:
    
    def __init__(self, app=None):
        super().__init__()
        if app is not None:
            self.init_app(app)
        self._project_dir = None

    def init_app(self, app):
        """Initializes the Flask app"""
        self._find_project_dir(app)
        self._check_project_structure()
        self._check_project_config(app)
        self._setup_rest_api(app)
        self._register_modules(app)
    

    def _find_project_dir(self, app):
        project_dir = os.path.dirname(app.instance_path)
        while 'app' in project_dir:
            project_dir = os.path.dirname(project_dir)
        print(project_dir, project_dir in sys.path)
        self._project_dir = project_dir


    def _check_project_structure(self):
        project_dir = self._project_dir
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


    def _setup_rest_api(self, app):
        config = app.config
        title = config['PIGAL_PROJECT_NAME'] + ' API'
        version = config['PIGAL_PROJECT_VERSION']
        api_bp = Blueprint('api', __name__, url_prefix='/api')
        api = Api(api_bp, title=title, version=version)
        app.register_blueprint(api_bp)
        self.api = api


    def _register_modules(self, app):
        app.logger.debug('looking for modules...')
        modules_dir = os.path.join(self._project_dir, 'modules')
        if os.path.isdir(modules_dir):
            for name in os.listdir(modules_dir):
                if name.startswith('_'):
                    continue 
                self._register_ui(app, name)
                self._register_api(app, name)

                
    def _register_ui(self, app, name):
        try:
            root = f'modules.{name}.pages.routes'
            module = importlib.import_module(root)
            ui = module.ui
        except (ModuleNotFoundError, AttributeError) as e:
            app.logger.warning(e)
            return
        
        if not isinstance(ui, ModuleUi):
            msg = f"The object 'ui' of {root} "
            msg += "is not an instance of ModuleUi"
            raise exc.InvalidModuleUi(msg)
        
        url_prefix=f'/{name}'
        app.register_blueprint(ui, url_prefix=url_prefix)
        app.logger.info(f'Register ui: {root} => {url_prefix}')
        return True
    

    def _register_api(self, app, name):
        try:
            root = f'modules.{name}.services.routes'
            module = importlib.import_module(root)
            api = module.api
        except (ModuleNotFoundError, AttributeError) as e:
            app.logger.warning(e)
            return False
        
        if not isinstance(api, ModuleApi):
            msg = f"The object 'api' of {root} "
            msg += "is not an instance of ModuleApi"
            raise exc.InvalidApi(msg)
        
        self.api.add_namespace(api)
        app.logger.info(f'Register api: {root} => {api.path}')
        return True


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
        self._register_modules(app)


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

    def _register_modules(self, app):
        app.logger.debug('looking for modules...')
        project_dir = os.path.dirname(app.instance_path)
        modules_dir = os.path.join(project_dir, 'modules')
        if os.path.isdir(modules_dir):
            for name in os.listdir(modules_dir):
                if name.startswith('_'):
                    continue 
                self._register_ui(app, name)
                self._register_api(app, name)
                self._register_rst(app, name)

                
    def _register_ui(self, app, name):
        try:
            root = f'modules.{name}.views'
            module = importlib.import_module(root)
            ui = module.ui
        except (ModuleNotFoundError, AttributeError) as e:
            app.logger.warning(e)
            return
                
        # 
        # check ui module
        #
        module_path = os.path.abspath(module.__file__)
        if not os.path.isfile(module_path):
            return
            
        # 
        # check ui parent class
        #  
        if not isinstance(ui, ModuleUi):
            msg = f"The object 'ui' of {root} "
            msg += "is not an instance of ModuleUi"
            raise exc.InvalidModuleUi(msg)
        
        #
        # file-based routing
        # ui blueprint registering
        # 
        ui.scan()
        url_prefix=f'/{name}'
        app.register_blueprint(ui, url_prefix=url_prefix)
        app.logger.info(f'Register ui: {root} => {url_prefix}')
        return True
    

    def _register_api(self, app, name):
        #
        # load api
        #
        try:
            root = f'modules.{name}.services'
            module = importlib.import_module(root)
            api = module.api
        except (ModuleNotFoundError, AttributeError) as e:
            app.logger.warning(e)
            return False

        # 
        # check api module
        #
        module_path = os.path.abspath(module.__file__)
        if not os.path.isfile(module_path):
            return
        
        # 
        # check api parent class
        #  
        if not isinstance(api, ModuleApi):
            msg = f"The object 'api' of {root} "
            msg += "is not an instance of ModuleApi"
            raise exc.InvalidApi(msg)
        
        self.api.add_namespace(api)
        app.logger.info(f'Register api: {root} => {api.path}')
        return True


    def _register_rst(self, app, name):
        root = f'modules.{name}.resources'
        try:
            _ = importlib.import_module(root)
        except ModuleNotFoundError as e:
            app.logger.warning(e)
            return False

    

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
                _ = importlib.import_module(f'backends.{name}.models') # important to load metada

                # create binds for sqlalchemy
                uri_args['backend_id'] = name
                uri = uri_template.format_map(uri_args)
                min_uri = self._minify_uri(uri)
                bind_keys[name] = uri
                app.logger.debug(f'Prepare database: {name} => {min_uri}')
        
        # store models binds
        app.config['SQLALCHEMY_BINDS'] = bind_keys    

