

Creating projects
=================


To create a project ``MyProject`` use ``create-project`` command:

.. code-block:: bash

    pigal create-project MyProject



Project structure
-----------------

This will create a project with the following structure:

.. code-block:: text

    myproject/
    ├── app/                  # app configuration and execution
    ├── migrations/           # databases migration files
    ├── modules/              # modules directory
    │   ├── auth/             # security frontend and backend
    │   └── home/             # home frontend and backend
    ├── tests/                # tests files
    ├── themes/               # themes directory
    │   └── default/          # default design system
    ├── translations/         # internationalisation files
    └── requirements.txt      # required python package list


.. IMPORTANT::

    **At beginner level, don't modify or delete the following directories**:
    
    * ``app`` (to customize it see ...)
    * ``modules/auth`` (to customize it see ...)
    * ``modules/home`` (to customize it see ...)
    * ``themes/default`` (to customize it see ...)

    


Running project
---------------

Navigate to ``myproject`` directory and run the Flask app:

.. code-block:: bash

    cd myproject
    flask run


Go to:

* http://127.0.0.1:5000 to see the default project page.
* http://127.0.0.1:5000/api to see the default project Rest API.


.. NOTE::
    By default, Flask app run at http://127.0.0.1:5000.


Customizing project
-------------------

Within this structure, we can now:

* create specific frontend (see :ref:`Creating frontends (UI)`)
* create specific backend (see :ref:`Creating backends (API)`)
* delete specific frontend (by deleting simply its directory)
* delete specific backend (by deleting also its directory)


**Next step in quickstart** : :ref:`Creating modules`