Introduction to Pigal-Flask
===========================


Installation
------------
Use the following command to install `Pigal-Flask` extension:

.. code-block:: bash

    pip install Pigal-Flask


Creating minimal project
------------------------

Use the following command to create a new pigal project:

.. code-block:: bash

    pigal create-project <my-project> <my-theme>
    

This will create a pigal project with the following structure:

.. code-block::

    /<my-project>
    │   
    ├── /app                  # core app
    │   ├── /static           # theme static files
    │   ├── /templates        # theme jinja templates
    │   ├── __init__.py       # app initialization
    │   ├── config.py         # app configurations
    │   ├── extensions.py     # app flask extensions
    │   
    ├── /pages                # front-ends or UIs
    │   ├── /home             # home front-end or UI
    │   ├── __init__.py       # global UI initialisation
    │   
    ├── /services             # microservices or APIs
    │   ├── /auth             # Authentification microservice
    │   ├── __init__.py       # global API initialisation
    │   

.. DANGER::
    This structure is required for any Pigal project. 
    Don't remove any of theses directories or files


Creating new domain pages
-------------------------

Use the following commands to create domain specific pages inside pages:

.. code-block:: bash

    cd <my-project>/pages
    pigal create-pages <my-domain>


This will create the following structure:

.. code-block::

    /pages
    │   
    ├── /<my-domain>          # domain pages
    │   ├── /static           # domain static files
    │   ├── /templates        # domain jinja templates
    │   ├── __init__.py       # domain initialization
    │   ├── forms.py          # domain WTF-forms
    │   ├── routes.py         # domain flask routes
    │   


.. IMPORTANT::
    pages can only be created inside the `pages` directory of a pigal project


Creating new domain service
---------------------------

Use the following commands to create a microservice inside services directory:

.. code-block:: bash
    
    cd <my-project>/services
    pigal create-service <my-domain> <my-version>


This will create the following structure:

.. code-block::

    /services
    │   
    ├── /<service_name>       # new microservice
    │   ├── /store            # new microservice files
    │   ├── __init__.py       # microservice initialization
    │   ├── models.py         # domain database models
    │   ├── routes.py         # domain Rest API
    │   ├── utils.py          # domain utilities
    │   


.. IMPORTANT::
    Service can only be created inside the `services` directory of a pigal project
