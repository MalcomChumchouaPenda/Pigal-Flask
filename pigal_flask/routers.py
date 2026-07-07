
import os
from flask import Blueprint


class WebUi(Blueprint):
    """A Web User Interface for a module or domain.
    
    This is a extended Flask Blueprint whose name and url_prefix are automatically generated.
    It is automatically detected during app loading. It is required for web routing.

    Parameters:
        routers_file: The filepath of related routers

    """

    def __init__(self, routers_file):
        # split path components
        path_components = []
        current_file = routers_file
        while current_file != os.path.dirname(current_file):
            path_components.append(os.path.basename(current_file))
            current_file = os.path.dirname(current_file)
        path_components.append(current_file)
        path_components.reverse()

        # search root name
        i = path_components.index('routers.py')
        root_name = path_components[i-1]

        # search import name
        j = path_components.index('modules')
        import_parts = path_components[j:]
        import_parts[-1] = import_parts[-1].replace(".py", "")
        import_name = ".".join(import_parts)

        # search static url
        static_url_path = os.path.join(*path_components[:i])
        static_url_path = os.path.join(static_url_path, 'assets')
        super().__init__(root_name, import_name, 
                         template_folder='pages', 
                         static_folder=static_url_path,
                         static_url_path=static_url_path)
        


class FileRouter:
    """ A File-based routing implementation for module/domain

    This is Router which implement file-based routing for a module Ui.
    """
