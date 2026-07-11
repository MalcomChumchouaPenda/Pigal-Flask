
from click import ClickException


class InvalidProjectStructure(Exception):
    pass

class InvalidProjectConfig(Exception):
    pass


class InvalidModuleUi(Exception):
    pass

class InvalidApi(Exception):
    pass



class InvalidCommandContext(ClickException):
    """This exception is raised when a command is executed
    in the wrong directory. Theses wrong cases of command execution 
    are the following:

    - execution of ``create-frontend`` outside of a ``frontends`` directory
    - execution of ``create-backend`` outside of a ``backends`` directory
    
    """


class InvalidThemeFile(ClickException):
    """This exception is raised if a theme file does not contains one of
    the following folders or files:

    - a ``static`` folder
    - a ``layouts`` folder
    - a ``layouts/landing.jinja`` file
    - a ``layouts/dashboard.jinja`` file
    - a ``layouts/auth.jinja`` file
    - a ``home`` folder
    - a ``home/login.jinja`` file
    - a ``home/index.jinja`` file
    - a ``home/dashboard.jinja`` file
    - a ``examples`` folder
    
    """

