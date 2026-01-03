Introduction to Pigal-Flask
===========================


Installation
------------
Use the following command to install ``Pigal-Flask`` extension:

.. code-block:: bash

    pip install Pigal-Flask



Creating minimal project
------------------------

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



Creating new domain pages
-------------------------

Use the following commands to create domain specific pages 
inside ``/<project-name>/pages``:

.. code-block:: bash

    pigal create-pages <domain>


This will create the following structure:

.. code-block::

    /pages
    |   
    |-- /<domain>             # CREATED PAGES DIRECTORY
    |   |-- /static           # domain static files
    |   |-- /templates        # domain jinja templates
    |   |   |-- /<domain>     # specific pages templates
    |   |
    |   |-- __init__.py       # domain initialization
    |   |-- forms.py          # domain WTF-forms
    |   |-- routes.py         # domain flask routes
    |   


.. IMPORTANT::
    pages can only be created inside the ``/pages`` directory of a pigal project



Creating new domain service
---------------------------

Use the following commands to create a microservice inside 
``/<project-name>/services`` directory:

.. code-block:: bash

    pigal create-service <domain> <version>


This will create the following structure:

.. code-block::

    /services
    |   
    |-- /<service_name>       # CREATED SERVICE DIRECTORY
    |   |-- /store            # new microservice files
    |   |-- __init__.py       # microservice initialization
    |   |-- models.py         # domain database models
    |   |-- routes.py         # domain Rest API
    |   |-- utils.py          # domain utilities
    |   


.. IMPORTANT::
    Service can only be created inside the ``/services`` 
    directory of a pigal project
