

Creating minimal project
========================

``create-project`` command
--------------------------

Before creating a new project, you must download a theme.


To create a new pigal project ``MyProject`` 
with a theme ``MyTheme.zip``, use the following command:

.. code-block:: bash

    pigal create-project MyProject C:/MyTheme.zip



Default Project structure
-------------------------

This will create a pigal project with the following structure:

.. code-block::

    /myproject
    |   
    |-- /app                  # APP SUB-DIRECTORY
    |   |-- /static           # theme static files
    |   |-- /templates        # theme jinja templates
    |   |-- __init__.py       # app initialization
    |   |-- config.py         # app configurations
    |   |-- extensions.py     # app flask extensions
    |   
    |-- /pages                # FRONTENDS SUB-DIRECTORY
    |   |-- /demo             # theme live demo
    |   |-- /home             # home frontend 
    |   |-- __init__.py       # global frontend initialisation
    |   
    |-- /services             # MICROSERVICES SUB-DIRECTORY
    |   |-- /auth             # authentification microservice
    |   |-- __init__.py       # global api initialisation
    |   


.. IMPORTANT::
    The directories ``app``, ``pages/home``, ``services/auth``
    are required for any Pigal project.



Running the Flask App
---------------------

Navigate to the project directory and run the flask app:

.. code-block:: bash

    cd myproject
    flask run

By default, the app will run at http://localhost:5000.

You should see the default "Hello World!" page.



Next steps in project
---------------------

Within this structure, we can now:

* create specific pages (see :ref:`Creating domain pages`)
* create microservices (see :ref:`Creating domain services`)
