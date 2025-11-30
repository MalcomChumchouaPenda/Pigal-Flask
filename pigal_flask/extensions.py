
import os
import re
from importlib import import_module
from flask import Blueprint
from .constants import PAGE_NAME_PATTERN



class Pigal:
    """
    The main class for adding utils to Flask for Pigal Projects

    Parameters
    ----------
    app: Flask
        flask Application to extend

    """

    def __init__(self, app=None):
        super().__init__()
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initializes the Flask app"""
        self._register_pages(app)

    def _register_pages(self, app):
        # print('cwd', os.getcwd(), os.path.abspath(app.config['PIGAL_ROOT_DIR']))
        app.logger.debug('looking for pages...')
        work_dir = os.path.abspath(app.config['PIGAL_ROOT_DIR'])
        pages_dir = os.path.join(work_dir, 'pages')
        if os.path.isdir(pages_dir):
            for name in os.listdir(pages_dir):
                if name.startswith('_'):
                    continue
                nameparts = re.findall(PAGE_NAME_PATTERN, name)
                if len(nameparts) != 1:
                    app.logger.info(f'Ignore folder: {name}')
                    continue
                rootname = nameparts[0].replace('_', '-')
                url_prefix = '/' if rootname == 'home' else f'/{rootname}' 
                ui_root = f'pages.{name}'
                print(url_prefix, ui_root)
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


class PigalUi(Blueprint):
    """
    The main class to extend Flask Blueprints for Pigal Projects frontend

    Parameters
    ----------
    import_name: str
        name used during import

    """

    def __init__(self, import_name, imported_file):
        page_root = os.path.dirname(imported_file)
        while 'routes' in page_root:
            page_root = os.path.dirname(page_root)
        root_name = os.path.basename(page_root)
        static_url_path = os.path.join(page_root, 'static')
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