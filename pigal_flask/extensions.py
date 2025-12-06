
import os
import re
import sys
import inspect
from importlib import import_module
from flask import Blueprint
from flask_restx import Api, Namespace
from flask_sqlalchemy import SQLAlchemy
from .utils import bind_key, tablename


_PAGE_PATTERN = '^([a-z][a-z0-9_]*)$'
_SERVICE_PATTERN = '^([a-z][a-z0-9_]*)_(v[0-9]+)$'
_API_BP = Blueprint('api', __name__)


class InvalidProjectStructure(Exception):
    pass


class Pigal:
    """
    The Main Class for adding utils to Flask App

    Parameters
    ----------
    app: Flask
        flask Application to extend

    Attributes
    ----------
    api: Flask-Restx.Api
        Rest Api for services

    """

    def __init__(self, app=None):
        super().__init__()
        self.api = None
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initializes the Flask app"""
        self._check_project_structure(app)
        # self._register_pages(app)
        # self._setup_api(app)
        # self._register_services(app)

    def _check_project_structure(self, app):
        project_dir = os.path.dirname(app.instance_path)
        print(project_dir)
        for required_name in ('app', 'pages', 'services'):
            required_dir = os.path.join(project_dir, required_name)
            print('test', required_dir)
            if not os.path.isdir(required_dir):
                msg = f"'{required_name}' directory is required but not found"
                raise InvalidProjectStructure(msg)
        

    def _register_pages(self, app):
        app.logger.debug('looking for pages...')
        root_dir = os.path.abspath(app.config['PIGAL_ROOT_DIR'])
        pages_dir = os.path.join(root_dir, 'pages')
        if os.path.isdir(pages_dir):
            for name in os.listdir(pages_dir):
                if name.startswith('_'):
                    continue
                nameparts = re.findall(_PAGE_PATTERN, name)
                if len(nameparts) != 1:
                    app.logger.info(f'Ignore folder: {name}')
                    continue
                rootname = nameparts[0].replace('_', '-')
                url_prefix = '/' if rootname == 'home' else f'/{rootname}' 
                ui_root = f'pages.{name}'
                self._register_page(app, ui_root, url_prefix)
                
    def _register_page(self, app, ui_root, url_prefix):
        try:
            routes = import_module(f'{ui_root}.routes')
            # menus = import_module(f'{ui_root}.menus')
            app.register_blueprint(routes.ui, url_prefix=url_prefix)
            app.logger.info(f'Register page: {ui_root} => {url_prefix}')
            return True
        except (ModuleNotFoundError, AttributeError) as e:
            app.logger.warning(e)


    def _setup_api(self, app):
        config = app.config
        self.api = Api(_API_BP, 
                       doc='/doc/', 
                       version=config['PIGAL_PROJECT_VERSION'], 
                       title= config['PIGAL_PROJECT_NAME'] + ' Api')
        app.register_blueprint(_API_BP, url_prefix='/api')

    def _register_services(self, app):
        app.logger.debug('looking for services...')
        root_dir = os.path.abspath(app.config['PIGAL_ROOT_DIR'])
        services_dir = os.path.join(root_dir, 'services')
        if os.path.isdir(services_dir):
            for name in os.listdir(services_dir):
                if name.startswith('_'):
                    continue
                nameparts = re.findall(_SERVICE_PATTERN, name)
                if len(nameparts) != 1:
                    app.logger.warning('Ignore folder: '+ name)
                    continue
                rootname, version = nameparts[0]
                rootname = rootname.replace('_', '-')
                version = version.replace('_', '.')
                url_prefix = f'/{rootname}/{version}'
                service_root = f'services.{name}'
                self._register_service(app, service_root, url_prefix)

    def _register_service(self, app, service_root, url_prefix):
        try:
            routes = import_module(f'{service_root}.routes')
            self.api.add_namespace(routes.api, path=url_prefix)
            app.logger.info(f'Register service: {service_root} => {url_prefix}')
            return True
        except (ModuleNotFoundError, AttributeError) as e:
            app.logger.warning(e)


class PigalUi(Blueprint):
    """
    The Extended Flask Blueprint for Pigal Projects frontend

    Parameters
    ----------
    import_name: str
        name used during import

    """

    def __init__(self, imported_file):
        # split path components
        path_components = []
        current_file = imported_file
        while current_file != os.path.dirname(current_file):
            path_components.append(os.path.basename(current_file))
            current_file = os.path.dirname(current_file)
        path_components.append(current_file)
        path_components.reverse()

        # search root name
        if 'routes' in path_components:
            i = path_components.index('routes')
        else:
            i = path_components.index('routes.py')
        root_name = path_components[i-1]

        # search import name
        j = path_components.index('pages')
        import_parts = path_components[j:]
        import_parts[-1] = import_parts[-1].replace(".py", "")
        import_name = ".".join(import_parts)

        # search static url
        static_url_path = os.path.join(*path_components[:i])
        static_url_path = os.path.join(static_url_path, 'static')
        super().__init__(root_name, import_name, 
                         template_folder='templates', 
                         static_folder='static',
                         static_url_path=static_url_path)
        # self.login_required = login_required


    # def roles_accepted(self, *roles):
    #     """Décorateur pour protéger les routes Flask qui renvoient des pages HTML."""
    #     def decorator(f):
    #         @wraps(f)
    #         @login_required
    #         def decorated_function(*args, **kwargs):
    #             if not current_user.is_authenticated:
    #                 # Redirection vers la page de connexion
    #                 msg = "Vous devez être connecté pour accéder à cette page."
    #                 return redirect(url_for('home.login', message=msg))  
    #             if len([n for n in roles if current_user.has_role(n)]) == 0:
    #                  # Redirection vers la page d'accueil
    #                 msg = "Vous n'avez pas la permission d'accéder à cette page."
    #                 return redirect(url_for('home.access_denied', message=msg)) 
    #             return f(*args, **kwargs)
    #         return decorated_function
    #     return decorator


class PigalApi(Namespace):
    """
    The Extended Flask-Restx Namespace for Pigal Projects backend

    Parameters
    ----------
    import_name: str
        name used during import

    """

    def __init__(self, imported_file):
        # split path components
        path_components = []
        current_file = imported_file
        while current_file != os.path.dirname(current_file):
            path_components.append(os.path.basename(current_file))
            current_file = os.path.dirname(current_file)
        path_components.append(current_file)
        path_components.reverse()

        # search root name
        i = path_components.index('routes.py')
        root_name = path_components[i-1]
        super().__init__(root_name)

    # @classmethod
    # def login_required(cls, f):
    #     """Décorateur pour protéger les routes API."""
    #     @wraps(f)
    #     def decorated_function(*args, **kwargs):
    #         if not current_user.is_authenticated:
    #             return {'message': 'Unauthorized'}, 401
    #         return f(*args, **kwargs)
    #     return decorated_function
    
    # @classmethod
    # def roles_accepted(cls, *roles):
    #     """Décorateur pour protéger les routes API avec des rôles spécifiques."""
    #     def decorator(f):
    #         @wraps(f)
    #         # @login_required
    #         def decorated_function(*args, **kwargs):
    #             if not current_user.is_authenticated:
    #                 return {'message': 'Unauthorized'}, 401
    #             if len([n for n in roles if current_user.has_role(n)]) == 0:
    #                 return {'message': 'Forbidden'}, 403
    #             return f(*args, **kwargs)
    #         return decorated_function
    #     return decorator


class PigalDb(SQLAlchemy):
    """The Extended Db for Pigal Projects backend"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        setattr(self.Model, '__tablename__', tablename)
        setattr(self.Model, '__bind_key__', bind_key)

    def init_app(self, app):
        self._prepare_db(app)
        return super().init_app(app)
    
    
    @classmethod
    def _minify_uri(cls, uri):
        if len(uri) > 50:
            return uri[:20] + '...' + uri[-20:]
        return uri
    
    def _prepare_db(self, app):
        app.logger.debug('looking for databases...')
        root_dir = os.path.abspath(app.config['PIGAL_ROOT_DIR'])
        uri_template = app.config['PIGAL_DB_URI_TEMPLATE']
        uri_args = {'root_dir':root_dir}

        # by default
        uri_args['service_id'] = 'default'
        uri = uri_template.format_map(uri_args)
        min_uri = self._minify_uri(uri)
        app.config['SQLALCHEMY_DATABASE_URI'] = uri
        app.logger.debug(f'Prepare database: default => {min_uri}')

        # by services
        services_dir = os.path.join(root_dir, 'services')
        bind_keys = {}
        if os.path.isdir(services_dir):
            for name in os.listdir(services_dir):
                # check if has models
                if name.startswith('_'):
                    continue
                if not re.match(_SERVICE_PATTERN, name):
                    continue
                modelspath = os.path.join(services_dir, name, 'models.py')
                if not os.path.isfile(modelspath):
                    continue
                _ = import_module(f'services.{name}.models') # important to load metada

                # create binds for sqlalchemy
                uri_args['service_id'] = name
                uri = uri_template.format_map(uri_args)
                min_uri = self._minify_uri(uri)
                bind_keys[name] = uri
                app.logger.debug(f'Prepare database: {name} => {min_uri}')
        
        # store models binds
        app.config['SQLALCHEMY_BINDS'] = bind_keys

