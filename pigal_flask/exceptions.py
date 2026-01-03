
from click import ClickException


class InvalidCommandContext(ClickException):
    """This exception is raised when a command is executed
    in the wrong directory. Theses wrong cases of command execution 
    are the following:

    - execution of ``create-pages`` outside of a ``pages`` directory
    - execution of ``create-service`` outside of a ``services`` directory
    
    """


class InvalidThemeFile(ClickException):
    """This exception is raised if a theme file does not contains one of
    the following folders or files:

    - a ``static`` folder
    - a ``layouts`` folder
    - a ``layouts/landing.jinja`` file
    - a ``layouts/admin.jinja`` file
    - a ``layouts/auth.jinja`` file
    - a ``home`` folder
    - a ``home/login.jinja`` file
    - a ``home/index.jinja`` file
    - a ``home/dashboard.jinja`` file
    - a ``examples`` folder
    
    """

