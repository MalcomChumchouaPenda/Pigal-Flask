

Creating minimal project
========================

Using command
-------------

Before creating a new project, you must download a theme.


To create a new pigal project ``mysite`` 
with a theme ``mytheme.zip``, use the following command:

.. code-block:: bash

    pigal create-project mysite C:/mytheme.zip



Default Project structure
-------------------------

This will create a pigal project with the following structure:

.. code-block::

    /mysite
    |   
    |-- /app                  # APP SUB-DIRECTORY
    |   |-- /static           # mytheme static files
    |   |-- /templates        # mytheme jinja templates
    |   |-- __init__.py       # app initialization
    |   |-- config.py         # app configurations
    |   |-- extensions.py     # app flask extensions
    |   
    |-- /pages                # FRONTENDS SUB-DIRECTORY
    |   |-- /demo             # mytheme live demo
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

    cd mysite
    flask run

By default, the app will run at ``http://localhost:5000``.

You should see the default "Hello World!" page.



Next steps
----------

Within this structure, we can now:
* create specific pages (see :ref:`Creating domain pages`)
* create microservices (see :ref:`Creating domain services`)
