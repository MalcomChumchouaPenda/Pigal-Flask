

__version__ = '0.0.1'


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
