

Creating frontend
=================


``create-frontend`` command
---------------------------

To create ``MyDomain`` frontend, 
navigate to ``frontends`` directory :

.. code-block:: bash

    cd frontends


then use the ``create-frontend`` command :

.. code-block:: bash

    pigal create-frontend MyDomain


Default frontend structure
--------------------------

This command will create the following structure:

.. code-block::

    /mydomain
    |
    |-- /static                # static files
    |-- /templates             # jinja templates
    |   |-- /mydomain          # domain templates
    |       |-- index.jinja    # default page file
    |
    |-- __init__.py            # domain initialization
    |-- forms.py               # domain WTF-forms
    |-- routes.py              # domain routes


Inside ``routes.py``, a default routing system is created:

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

    +----------------------------------+----------------+----------------+
    | domain path                      | blueprint name | url prefix     |
    +==================================+================+================+
    | ``myproject/frontends/home``     | ``home``       | ``/``          |
    +----------------------------------+----------------+----------------+
    | ``myproject/frontends/demo``     | ``demo``       | ``/demo``      |
    +----------------------------------+----------------+----------------+
    | ``myproject/frontends/mydomain`` | ``mydomain``   | ``/mydomain``  |
    +----------------------------------+----------------+----------------+


The command ``create-frontend`` also create a default ``index.jinja``:

.. code-block:: HTML

    {% extends 'layouts/default.jinja' %}
    {% set title = 'Welcome in MyDomain' %}
    {% set sub_title = 'This is the default page' %}


Running the Frontend
--------------------

Run project and go to http://127.0.0.1:5000/mydomain to see ``MyDomain`` default page.


Customizing Frontends
---------------------

With this frontend structure, you can then:

* create custom pages within ``templates`` (see `Jinja Templates documentation`_)
* create custom views within ``routes.py`` (see `Flask blueprint documentation`_)
* create custom WTF-forms within ``forms.py`` (see `Flask-WTF documentation`_)

.. _Jinja Templates documentation: https://jinja.palletsprojects.com/en/stable/
.. _Flask blueprint documentation: https://flask.palletsprojects.com/en/stable/tutorial/views/
.. _Flask-WTF documentation: https://flask-wtf.readthedocs.io/en/1.2.x/


To develop custom pages, you can also:

* http://127.0.0.1:5000/demo to see examples of frontend pages.
* http://127.0.0.1:5000/demo/docs to see tutorials on theme usage.


**Next step in quickstart** : :ref:`Creating backend`

