

Creating domain pages
=====================

To create ``mydomain`` pages, 
use the ``create-pages`` command 
inside ``mysite/pages``:

.. code-block:: bash

    pigal create-pages mydomain


.. IMPORTANT::
    pages can only be created inside the ``pages`` directory


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

    +---------------------------+----------------+----------------+
    | domain path               | blueprint name | url prefix     |
    +===========================+================+================+
    | ``mysite/pages/home``     | ``home``       | ``/``          |
    +---------------------------+----------------+----------------+
    | ``mysite/pages/demo``     | ``demo``       | ``/demo``      |
    +---------------------------+----------------+----------------+
    | ``mysite/pages/mydomain`` | ``mydomain``   | ``/mydomain``  |
    +---------------------------+----------------+----------------+


The command ``create-pages`` also create a minimal ``index.jinja`` 
template inside ``templates/mydomain``:

.. code-block:: HTML

    {% extends 'layouts/default.jinja' %}
    {% set title = 'Welcome in mydomain' %}
    {% set sub_title = 'This is the default page' %}


Go to http://127.0.0.1:5000/mydomain to see this default page of ``mydomain``.


With this pages structure, you can then:

* modify default page template (see `Jinja Templates documentation`_)
* add or deletes views to ``ui`` blueprint (see `Flask blueprint documentation`_)
* create custom page inspired by ``demo`` templates (provided by choosen theme)
* create WTF-forms inside ``forms.py`` and use it (see `Flask-WTF documentation`_)

.. _Jinja Templates documentation: https://jinja.palletsprojects.com/en/stable/
.. _Flask blueprint documentation: https://flask.palletsprojects.com/en/stable/tutorial/views/
.. _Flask-WTF documentation: https://flask-wtf.readthedocs.io/en/1.2.x/

