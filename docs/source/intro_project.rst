
Creating minimal project
========================

    
Use the following command to create a new pigal project:

.. code-block:: bash

    pigal create-project <project-name> <theme-file>
    

This will create a pigal project with the following structure:

.. code-block::

    /<project-name>
    |   
    |-- /app                  # CORE APP SUB-DIRECTORY
    |   |-- /static           # theme static files
    |   |-- /templates        # theme jinja templates
    |   |-- __init__.py       # app initialization
    |   |-- config.py         # app configurations
    |   |-- extensions.py     # app flask extensions
    |   
    |-- /pages                # FRONT-ENDS AND UI SUB-DIRECTORY
    |   |-- /home             # home front-end or UI
    |   |-- __init__.py       # global UI initialisation
    |   
    |-- /services             # MICROSERVICES AND API SUB-DIRECTORY
    |   |-- /auth             # Authentification microservice
    |   |-- __init__.py       # global API initialisation
    |   

.. DANGER::
    This structure is required for any Pigal project. 
    Don't remove any of theses directories or files
