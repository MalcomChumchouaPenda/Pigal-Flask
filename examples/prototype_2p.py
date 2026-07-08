import inspect
import wrapt
from flask import Blueprint

# Définition de votre Blueprint ou Application Flask
bp = Blueprint('api', __name__)

# Création du décorateur de route étendu avec wrapt
def route_etendue(blueprint, rule, **options):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        # instance est None s'il s'agit d'une fonction libre ou d'une méthode statique.
        # S'il s'agit d'une méthode de classe / instance, 'instance' représente l'objet.
        return wrapped(*args, **kwargs)

    def decorator(func_or_class):
        # Extension aux classes (si l'utilisateur décore toute la classe)
        if inspect.isclass(func_or_class):
            cls = func_or_class
            # Parcours les méthodes de la classe
            for attr_name in dir(cls):
                attr = getattr(cls, attr_name)
                # Vérifie si la méthode a été marquée avec des règles de route
                if hasattr(attr, '__route_rule__'):
                    # Crée l'instance de la classe pour l'injecter dans view_func
                    instance = cls()
                    bound_method = getattr(instance, attr_name)
                    # Enregistre la route auprès du blueprint
                    blueprint.add_url_rule(
                        attr.__route_rule__, 
                        view_func=bound_method, 
                        **getattr(attr, '__route_options__', {})
                    )
            return cls
        else:
            # Comportement classique pour une simple fonction / méthode individuelle
            func = wrapper(func_or_class)
            blueprint.add_url_rule(rule, view_func=func, **options)
            return func

    # Attache les métadonnées de route à l'objet pour les traiter plus tard
    decorator.__route_rule__ = rule
    decorator.__route_options__ = options
    return decorator


class MonControleur:
    @route_etendue(bp, '/accueil', methods=['GET'])
    def index(self, **kwargs):
        return "Bienvenue sur l'accueil de la classe !"

@route_etendue(bp, '/api')
class ApiControleur:
    
    @route_etendue(bp, '/users', methods=['GET'])
    def get_users(self):
        return {"status": "success", "data": []}

    @route_etendue(bp, '/status', methods=['GET'])
    def check_status(self):
        return {"status": "online"}