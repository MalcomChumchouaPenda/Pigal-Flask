
Creating Databases
==================

For each ``service`` by default, 
a sqlite database is automatically created 
depending of the context of flask app execution. 

Here is some examples of their relative path:

.. table:: 
    :align: left

    +----------------------------+-----------------------------+--------------+------------------------+
    | service directory          | debug mode                  | testing mode | production mode        |
    +============================+=============================+==============+========================+
    | ``services/auth``          | ``/store/temp/auth.db``     | ``:memory:`` | ``store/auth.db``      |
    +----------------------------+-----------------------------+--------------+------------------------+
    | ``services/mydomain_v1``   | ``/store/temp/mydomain.db`` | ``:memory:`` | ``store/mydomain.db``  |
    +----------------------------+-----------------------------+--------------+------------------------+
    | ``services/mydomain_v1_2`` | ``/store/temp/mydomain.db`` | ``:memory:`` | ``store/mydomain.db``  |
    +----------------------------+-----------------------------+--------------+------------------------+


The ``app.extensions`` module will provide a ``db`` object
which permits to:

* model your database without conflict with other database (see :ref:`Modelling Databases`)
* use this database to provide utilities (see :ref:`Using database inside utils`)
* use this database to provide an api (see :ref:`Using database inside api`)
* use this database inside pages (see :ref:`Using database inside pages`)

.. NOTE::
    ``db`` is an instance of :any:`PigalDb` class. 
    This class is an subclass of the ``SQLAlchemy`` extension
    provided by ``Flask-SQLAlchemy``


Modelling Databases
-------------------

With ``db`` extension, you can define model data in ``models.py``:

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
    | model class | service name | ``__tablename__``      | ``__bind_key__``  |
    +=============+==============+========================+===================+
    | ``Item``    | mydomain 1.0 | ``mydomain_v1_0_item`` | ``mydomain_v1_0`` |
    +-------------+--------------+------------------------+-------------------+
    | ``Item``    | mydomain 1.5 | ``mydomain_v1_5_item`` | ``mydomain_v1_5`` |
    +-------------+--------------+------------------------+-------------------+
    | ``Post``    | mydomain 2.0 | ``mydomain_v1_0_post`` | ``mydomain_v2_0`` |
    +-------------+--------------+------------------------+-------------------+


.. DANGER::
    To avoid conflict between databases 
    from different versions of the same service,
    don't edit generated ``__tablename__`` and ``__bind_key__``


Using database inside utils
---------------------------

Using database inside api
-------------------------

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




Using database inside pages
---------------------------

