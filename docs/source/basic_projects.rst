

Creating project
================


``create-project`` command
--------------------------

Before creating a new project, you must download a theme (``MyTheme.zip`` for example). 

To create a project ``MyProject`` with ``MyTheme`` theme, use ``create-project`` command:

.. code-block:: bash

    pigal create-project MyProject C:/MyTheme.zip



Default Project structure
-------------------------

This will create a pigal project with the following structure:

.. code-block::

    /myproject
    |   
    |-- /app                  # APP DIRECTORY
    |   |-- /static           # theme static files
    |   |-- /templates        # theme jinja templates
    |   |-- __init__.py       # app initialization
    |   |-- config.py         # app configurations
    |   |-- extensions.py     # app flask extensions
    |   
    |-- /backends             # BACKENDS DIRECTORY
    |   |-- /auth             # authentification backend
    |   |-- __init__.py       # global api initialisation
    |   
    |-- /frontends            # FRONTENDS DIRECTORY
    |   |-- /demo             # theme live demo
    |   |-- /home             # home frontend 
    |   |-- __init__.py       # global frontend initialisation
    |   
    |-- /migrations           # databases migration files
    |-- /tests                # project tests  
    |-- /translations         # internationalisation files


.. IMPORTANT::
    The directories ``app``, ``frontends/home``, ``backends/auth``
    are required for any Pigal project.



Running the Flask App
---------------------

Navigate to the project directory and run the flask app:

.. code-block:: bash

    cd myproject
    flask run

By default, the app will run at http://localhost:5000.

Go to http://127.0.0.1:5000 to see the default project page.

Go to http://127.0.0.1:5000/api to see the default project Rest API.

Go to http://127.0.0.1:5000/demo to see examples of theme frontend pages.

Go to http://127.0.0.1:5000/demo/docs to see documentation page of theme used.


Next steps in project
---------------------

Within this structure, we can now:

* create specific frontend (see :ref:`Creating frontend`)
* create specific backend (see :ref:`Creating backend`)
