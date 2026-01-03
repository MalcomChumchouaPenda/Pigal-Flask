
Creating minimal project
========================

1. Creation steps
-------------------
    
Use the following command to create a new pigal project:

.. code-block:: bash

    pigal create-project <project-name> <theme-file>
    

2. Creation results
--------------------

This will create a pigal project with the following structure:

.. code-block::

    /<project-name>
    |   
    |-- /app                  # APP SUB-DIRECTORY
    |   |-- /static           # theme static files
    |   |-- /templates        # theme jinja templates
    |   |-- __init__.py       # app initialization
    |   |-- config.py         # app configurations
    |   |-- extensions.py     # app flask extensions
    |   
    |-- /pages                # FRONTENDS SUB-DIRECTORY
    |   |-- /demo             # theme demo frontend
    |   |-- /home             # home frontend 
    |   |-- __init__.py       # global frontend initialisation
    |   
    |-- /services             # MICROSERVICES SUB-DIRECTORY
    |   |-- /auth             # authentification microservice
    |   |-- __init__.py       # global api initialisation
    |   


.. DANGER::
    The directories ``/app``, ``/pages/home``, ``/services/auth``
    are required for any Pigal project. 
    Don't remove any of theses directories!

Within this structure, we can now create:

* domain pages inside ``/pages`` directory
  (see :ref:`Creating domain pages`)
* domain microservices inside ``/services`` directory
  (see :ref:`Creating domain services`)