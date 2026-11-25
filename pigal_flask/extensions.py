import os
import re
import sys
import inspect
import warnings
import importlib
from functools import wraps

from flask import Blueprint, abort
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SAWarning

from . import exceptions as exc
from . import utils
from .security.abstract import AccessStore, AccessProvider
from .interfaces import Ui, PublicApi, RestApi


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
        while "app" in project_dir:
            project_dir = os.path.dirname(project_dir)
        self._project_dir = project_dir

    def _check_project_structure(self):
        project_dir = self._project_dir
        for required_name in ("app", "modules"):
            required_dir = os.path.join(project_dir, required_name)
            if not os.path.isdir(required_dir):
                msg = f"'{required_name}' directory is required but not found"
                raise exc.InvalidProjectStructure(msg)

    def _check_project_config(self, app):
        for name in ("PIGAL_PROJECT_NAME", "PIGAL_PROJECT_VERSION"):
            if name not in app.config:
                msg = f"Configuration parameter '{name}' is missing"
                raise exc.InvalidProjectConfig(msg)

    def _setup_rest_api(self, app):
        config = app.config
        title = config["PIGAL_PROJECT_NAME"] + " API"
        version = config["PIGAL_PROJECT_VERSION"]
        api_bp = Blueprint("api", __name__, url_prefix="/api")
        api = Api(api_bp, title=title, version=version)
        app.register_blueprint(api_bp)
        self.api = api

    def _register_modules(self, app):
        app.logger.debug("looking for modules...")
        modules_dir = os.path.join(self._project_dir, "modules")
        if os.path.isdir(modules_dir):
            for name in os.listdir(modules_dir):
                if name.startswith("_"):
                    continue
                # module_dir = os.path.join(modules_dir, name)
                self._register_rest_api(app, name)
                self._register_ui(app, name)

    def _register_ui(self, app, name):
        try:
            root = f"modules.{name}.views"
            module = importlib.import_module(root)
            ui = module.ui
        except (ModuleNotFoundError, AttributeError) as e:
            app.logger.warning(e)
            return

        if not isinstance(ui, Ui):
            msg = f"{root}.ui is not an instance of Ui"
            raise exc.InvalidUi(msg)

        ui.scan_pages()
        url_prefix = "/" if name == "home" else f"/{name}"
        app.register_blueprint(ui, url_prefix=url_prefix)
        app.logger.info(f"Register ui: {root} => {url_prefix}")
        return True

    # def _search_apis(self, app, resources_dir):
    #     if not os.path.isdir(resources_dir):
    #         return

    #     for filename in os.listdir(resources_dir):
    #         if filename.startswith("_"):
    #             continue
    #         found = re.findall(r"(\S+)_(v\d+)", filename)
    #         if len(found):
    #             name, version = found[0]
    #             self._register_api(app, name, version)

    def _register_rest_api(self, app, name):
        try:
            root = f"modules.{name}.resources"
            module = importlib.import_module(root)
            api = module.rest_api
        except (ModuleNotFoundError, AttributeError) as e:
            app.logger.warning(e)
            return False

        if not isinstance(api, RestApi):
            msg = f"{root}.rest_api is not an instance of RestApi"
            raise exc.InvalidRestApi(msg)

        print('adding', self.api, api, f"/{name}/v0")
        self.api.add_namespace(api, path=f"/{name}/v0")
        app.logger.info(f"Register api: {root} => {api.path}")
        return True


class AccessManager:

    def __init__(self, app=None):
        super().__init__()
        self.store = None
        self.provider = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.extensions["access"] = self
        module = self._load_access_module()
        self._load_store(app, module)
        self._load_provider(app, module)

    def _load_access_module(self):
        root = f"modules.auth.services.access"
        module = importlib.import_module(root)
        return module

    def _load_store(self, app, module):
        cls_name = app.config.get("PIGAL_ACCESS_STORE_CLASS")
        if cls_name is None:
            msg = "PIGAL_ACCESS_STORE_CLASS is not configured"
            raise exc.InvalidAppConfig(msg)
        Store = getattr(module, cls_name)
        if not issubclass(Store, AccessStore):
            msg = f"{Store} is not valid AccessStore"
            raise TypeError(msg)
        self.store = Store()

    def _load_provider(self, app, module):
        cls_name = app.config.get("PIGAL_ACCESS_PROVIDER_CLASS")
        if cls_name is None:
            msg = "PIGAL_ACCESS_PROVIDER_CLASS is not configured"
            raise exc.InvalidAppConfig(msg)

        Provider = getattr(module, cls_name)
        if not issubclass(Provider, AccessProvider):
            msg = f"{Provider} is not valid AccessProvider"
            raise TypeError(msg)
        self.provider = Provider(store=self.store)

    def identity(self):
        return self.provider.identity()

    def is_authenticated(self):
        return self.provider.is_authenticated()

    def has_role(self, role):
        return self.provider.has_role(role)

    def has_permission(self, permission):
        return self.provider.has_permission(permission)

    def require_login(self):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if not self.is_authenticated():
                    abort(401)
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def require_role(self, role):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if not self.is_authenticated():
                    abort(401)
                if not self.has_role(role):
                    abort(403)
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def require_permission(self, permission):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if not self.is_authenticated():
                    abort(401)
                if not self.has_permission(permission):
                    abort(403)
                return func(*args, **kwargs)

            return wrapper

        return decorator


warnings.filterwarnings(
    "ignore",  # Action: Ignore the warning
    category=SAWarning,  # Category of the warning
    message=".*bind_key.*",  # Message pattern to match
    module="flask_sqlalchemy",  # Only suppress from this specific module
)


class PigalDb(SQLAlchemy):

    def __init__(self, *args, **kwargs):
        kwargs["disable_autonaming"] = True
        super().__init__(*args, **kwargs)
        setattr(self.Model, "__tablename__", utils.tablename)
        setattr(self.Model, "__bind_key__", utils.bind_key)

    def init_app(self, app):
        self._check_db_config(app)
        self._prepare_db(app)
        super().init_app(app)

    def _check_db_config(self, app):
        for name in ("PIGAL_DB_URI_TEMPLATE",):
            if name not in app.config:
                msg = f"Configuration parameter '{name}' is missing"
                raise exc.InvalidProjectConfig(msg)

    @classmethod
    def _minify_uri(cls, uri):
        if len(uri) > 50:
            return uri[:20] + "..." + uri[-20:]
        return uri

    def _prepare_db(self, app):
        app.logger.debug("looking for databases...")
        project_dir = os.path.dirname(app.instance_path)
        uri_template = app.config["PIGAL_DB_URI_TEMPLATE"]
        uri_args = {"project_dir": project_dir}

        # by default
        uri_args["backend_id"] = "default"
        uri = uri_template.format_map(uri_args)
        min_uri = self._minify_uri(uri)
        app.config["SQLALCHEMY_DATABASE_URI"] = uri
        app.logger.debug(f"Prepare database: default => {min_uri}")

        # by backends
        backends_dir = os.path.join(project_dir, "backends")
        bind_keys = {}
        if os.path.isdir(backends_dir):
            for name in os.listdir(backends_dir):
                #                 # check if has models
                if name.startswith("_"):
                    continue
                #                 if not re.match(_SERVICE_PATTERN, name):
                #                     continue
                modelspath = os.path.join(backends_dir, name, "models.py")
                if not os.path.isfile(modelspath):
                    continue
                _ = importlib.import_module(
                    f"backends.{name}.models"
                )  # important to load metada

                # create binds for sqlalchemy
                uri_args["backend_id"] = name
                uri = uri_template.format_map(uri_args)
                min_uri = self._minify_uri(uri)
                bind_keys[name] = uri
                app.logger.debug(f"Prepare database: {name} => {min_uri}")

        # store models binds
        app.config["SQLALCHEMY_BINDS"] = bind_keys
