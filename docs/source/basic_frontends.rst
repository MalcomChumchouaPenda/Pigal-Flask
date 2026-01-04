

Creating frontend
=================


``create-frontend`` command
---------------------------

To create ``MyDomain`` frontend, 
navigate to ``myproject/frontends`` directory
then use the ``create-frontend`` command :

.. code-block:: bash

    cd frontends
    pigal create-frontend MyDomain


.. IMPORTANT::
    frontend can only be created inside ``frontends`` directory


Default frontend structure
--------------------------

This command will create the following structure:

.. code-block::

    /frontends
    |   
    |-- /mydomain             # CREATED DIRECTORY
    |   |-- /static           # domain static files
    |   |-- /templates        # jinja templates
    |   |   |-- /mydomain     # domain templates
    |   |
    |   |-- __init__.py       # domain initialization
    |   |-- forms.py          # domain WTF-forms
    |   |-- routes.py         # domain flask routes


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


The command ``create-frontend`` also create a default ``index.jinja`` 
template inside ``templates/mydomain``:

.. code-block:: HTML

    {% extends 'layouts/default.jinja' %}
    {% set title = 'Welcome in MyDomain' %}
    {% set sub_title = 'This is the default page' %}


Running the Frontend
--------------------

Go to http://127.0.0.1:5000/mydomain to see default page of ``MyDomain``.



Customizing Frontend
--------------------

With this frontend structure, you can then:

* modify default page template (see `Jinja Templates documentation`_)
* add or deletes views to ``ui`` blueprint (see `Flask blueprint documentation`_)
* create custom page inspired by ``demo`` templates (provided by choosen theme)
* create WTF-forms inside ``forms.py`` and use it (see `Flask-WTF documentation`_)

.. _Jinja Templates documentation: https://jinja.palletsprojects.com/en/stable/
.. _Flask blueprint documentation: https://flask.palletsprojects.com/en/stable/tutorial/views/
.. _Flask-WTF documentation: https://flask-wtf.readthedocs.io/en/1.2.x/

