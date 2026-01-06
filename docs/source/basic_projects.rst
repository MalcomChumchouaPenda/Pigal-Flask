

Creating project
================


``create-project`` command
--------------------------

Before creating a new project, you must download a theme (``MyTheme_xy.zip`` for example). 

To create a project ``MyProject`` with ``MyTheme`` theme, use ``create-project`` command:

.. code-block:: bash

    pigal create-project MyProject C:/MyTheme_xy.zip



Default Project structure
-------------------------

This will create a pigal project with the following structure:

.. code-block::

    /myproject
    |   
    |-- /app                  # app system files
    |-- /backends             # backend directories
    |-- /frontends            # frontend directories 
    |-- /migrations           # databases migration files
    |-- /tests                # project tests files 
    |-- /translations         # internationalisation files
    |-- requirements.txt      # required python package


.. IMPORTANT::
    ``myproject`` directory contains special sub-directories:
    
    * ``app`` which provide app configuration and execution
    * ``backends/auth`` which provide security backend
    * ``frontends/home`` which provide home frontend
    * ``frontends/demo`` which provide theme demo frontend

    **At beginner level, don't modify or delete these sub-directories**


Running project
---------------

Navigate to ``myproject`` directory and run the Flask app:

.. code-block:: bash

    cd myproject
    flask run


Go to:

* http://127.0.0.1:5000 to see the default project page.
* http://127.0.0.1:5000/demo to see examples of theme pages.
* http://127.0.0.1:5000/api to see the default project Rest API.


.. NOTE::
    By default, Flask app run at http://127.0.0.1:5000.


Customizing project
-------------------

Within this structure, we can now:

* create specific frontend (see :ref:`Creating frontend`)
* create specific backend (see :ref:`Creating backend`)
* delete specific frontend (by deleting simply its directory)
* delete specific backend (by deleting also its directory)


**Next step in quickstart** : :ref:`Creating frontend`