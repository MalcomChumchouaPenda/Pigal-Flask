
Creating databases
==================


A sqlite database is automatically created for each backend and Flask execution context: 

.. table:: 
    :align: left

    +--------------------+-----------------------------------------------+
    | execution context  | created database                              |
    +====================+===============================================+
    | production mode    | ``backends/mydomain_v1_0/store/data.db``      |
    +--------------------+-----------------------------------------------+
    | development mode   | ``backends/mydomain_v1_0/store/temp/data.db`` |
    +--------------------+-----------------------------------------------+
    | testing mode       | ``:memory:``                                  |
    +--------------------+-----------------------------------------------+



Modelling Databases
-------------------

The ``app.extensions`` module will provide a ``db`` object which:

* is an instance of :any:`PigalDb` class (an extended ``Flask-SQLAlchemy`` extension)
* allows to model your database without conflict (within Multi-Databases architecture)


With this ``db`` extension, you can define model data in ``models.py``:

.. code-block:: python

    from app.extensions import db

    class Item(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50), nullable=False)
        is_active = db.Column(db.Boolean, default=True)


Models ``__tablename__`` and ``__bind_key__`` are automatically generated:

.. table::
    :align: left

    +-------------+--------------+------------------------+-------------------+
    | model class | backend name | ``__tablename__``      | ``__bind_key__``  |
    +=============+==============+========================+===================+
    | ``Item``    | MyDomain 1.0 | ``mydomain_v1_0_item`` | ``mydomain_v1_0`` |
    +-------------+--------------+------------------------+-------------------+
    | ``Item``    | MyDomain 1.5 | ``mydomain_v1_5_item`` | ``mydomain_v1_5`` |
    +-------------+--------------+------------------------+-------------------+
    | ``Post``    | MyDomain 1.5 | ``mydomain_v1_5_post`` | ``mydomain_v1_5`` |
    +-------------+--------------+------------------------+-------------------+

.. DANGER::
    Don't change Models ``__tablename__`` and ``__bind_key__`` to avoid naming conflicts.


See `Flask-SQLAlchemy documentation`_ for more details on database modelling.

.. _Flask-SQLAlchemy documentation: https://flask.palletsprojects.com/en/stable/tutorial/views/


Databases initialisation
------------------------

It can be necessary to **initialise databases with default data**.
This allow to:

* start project with default records.
* use different default records depending of execution context.


To initialise database of ``mydomain_v1_0`` backend, 
create a ``init_db`` method in its ``__init__.py`` file:

.. code-block:: python

    from .models import Item

    def init_db(session, app):
        if not Item.query.first():
            session.add_all([
                Item(name="Item A"),
                Item(name="Item B"),
                Item(name="Item C"),
            ])
            session.commit()


.. IMPORTANT::
    Pigal-Flask will automatically detect ``init_db`` method 
    and execute it at appropriate time.


Using databases within API
--------------------------

Now, in ``routes.py``, we can create an api 
to provide **CRUD** functionnalities. For example:

.. code-block:: python

    from flask import request
    from flask_restx import Resource
    from pigal_flask import PigalApi
    from app.extensions import db
    from . import models as mdl


    api = PigalApi(__file__)


    @api.route('/items')
    class ItemList(Resource):

        def get(self):
            '''Get all items'''
            items = mdl.Item.query.all()
            return [{"id":item.id, "name":item.name} for item in items]
        
        def post(self):
            '''add new item'''
            data = request.get_json()
            item = mdl.Item(name=data['name'])
            db.session.add(item)
            db.session.commit()
            return {"id":item.id, "name":item.name}, 201


Run the project and go to http://127.0.0.1:5000/api to test this API.


See `Flask-Restx documentation`_ for more details on :

* API responses marshalling with database models (convert db record to json data)
* API request parsing with database models (convert json data to valid db record)


.. _Flask-Restx documentation: https://flask-wtf.readthedocs.io/en/1.2.x/


Using databases within UI
-------------------------

Go to ``mydomain`` frontend folder, and edit for example ``routes.py``:

.. code-block:: python

    from flask import render_template
    from pigal_flask import PigalUi
    from backends.mydomain_v1 import models as mdl


    ui = PigalUi(__file__)


    @ui.route('/items')
    def list_items():
        items = mdl.Item.query.all()
        return render_template("mydomain/items.html", items=items)


Let's define ``mydomain/items.html`` template:

.. code-block:: HTML

    {% extends 'layouts/dashboard.jinja' %}

    {% block page_main %}
        <h1> Items </h1>
        <ol>
        {% for item in items %}
            <li> {{ item.name }} </li>
        {% endfor %}
        </ol>
    {% endblock %}


Run the project and go to http://127.0.0.1:5000/mydomain/items to see results.


**Next step in quickstart** : :ref:`Sharing projects`
