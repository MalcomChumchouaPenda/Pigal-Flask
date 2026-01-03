
Creating domain pages
=========================

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


