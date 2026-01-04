

Creating domain pages
=====================


``create-pages`` command
------------------------

To create ``MyDomain`` pages, 
use the ``create-pages`` command 
inside ``myproject/pages``:

.. code-block:: bash

    pigal create-pages MyDomain


.. IMPORTANT::
    pages can only be created inside the ``pages`` directory


Default Pages structure
-----------------------

This command will create the following structure:

.. code-block::

    /pages
    |   
    |-- /mydomain             # CREATED PAGES DIRECTORY
    |   |-- /static           # domain static files
    |   |-- /templates        # domain jinja templates
    |   |   |-- /mydomain     # specific pages templates
    |   |
    |   |-- __init__.py       # domain initialization
    |   |-- forms.py          # domain WTF-forms
    |   |-- routes.py         # domain flask routes
    |   

Inside ``routes.py``, a minimal flask routing system
is automatically created like this:

.. code-block:: python

    from flask import render_template
    from pigal_flask import PigalUi


    ui = PigalUi(__file__)


    @ui.route('/')
    def index():
        return render_template('mydomain/index.jinja')


The ``routes.py`` provides an ``ui`` object :

* which is an extended Flask blueprint ( :any:`PigalUi` )
* whose name and url_prefix are automatically created
* which is automatically registered into Flask app

Some examples of name and url_prefix generated:

.. table:: 
    :align: left

    +------------------------------+----------------+----------------+
    | domain path                  | blueprint name | url prefix     |
    +==============================+================+================+
    | ``myproject/pages/home``     | ``home``       | ``/``          |
    +------------------------------+----------------+----------------+
    | ``myproject/pages/demo``     | ``demo``       | ``/demo``      |
    +------------------------------+----------------+----------------+
    | ``myproject/pages/mydomain`` | ``mydomain``   | ``/mydomain``  |
    +------------------------------+----------------+----------------+


The command ``create-pages`` also create a minimal ``index.jinja`` 
template inside ``templates/mydomain``:

.. code-block:: HTML

    {% extends 'layouts/default.jinja' %}
    {% set title = 'Welcome in MyDomain' %}
    {% set sub_title = 'This is the default page' %}


Running the Frontend
--------------------

Go to http://127.0.0.1:5000/mydomain to see this default page of ``MyDomain``.



Customizing Frontend
--------------------

With this pages structure, you can then:

* modify default page template (see `Jinja Templates documentation`_)
* add or deletes views to ``ui`` blueprint (see `Flask blueprint documentation`_)
* create custom page inspired by ``demo`` templates (provided by choosen theme)
* create WTF-forms inside ``forms.py`` and use it (see `Flask-WTF documentation`_)

.. _Jinja Templates documentation: https://jinja.palletsprojects.com/en/stable/
.. _Flask blueprint documentation: https://flask.palletsprojects.com/en/stable/tutorial/views/
.. _Flask-WTF documentation: https://flask-wtf.readthedocs.io/en/1.2.x/

