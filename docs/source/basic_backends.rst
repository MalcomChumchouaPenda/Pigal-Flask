

Creating backend
================


``create-backend`` command
--------------------------

Any backend must have a **domain name** and a **version number**.

To create a ``MyDomain 1.0`` backend, navigate to ``backends`` directory:

.. code-block:: bash

    cd myproject/backends


use the command ``create-backend``:

.. code-block:: bash

    pigal create-backend MyDomain 1.0


.. IMPORTANT::
    Service can only be created inside the ``backends`` directory



Default backend structure
--------------------------

This command will create the following structure:

.. code-block::

    /backends
    |   
    |-- /mydomain_v1_0        # CREATED DIRECTORY
    |   |-- /store            # new backend files
    |   |-- __init__.py       # backend initialization
    |   |-- models.py         # domain database models
    |   |-- routes.py         # domain Rest API
    |   |-- utils.py          # domain utilities



Inside ``routes.py``, a minimal REST API is automatically created:

.. code-block:: python

    from flask_restx import Resource
    from pigal_flask import PigalApi


    api = PigalApi(__file__)


    @api.route('/ping')
    class Ping(Resource):
        def get(self):
            return {'message':'pong'}


This ``routes.py`` provides an ``api`` object :

* which is an extended Flask-Restx Namespace ( :any:`PigalApi` )
* whose id and url_prefix are automatically created
* which is automatically registered into Flask app


Some examples of id and url_prefix generated:

.. table:: 
    :align: left

    +--------------------------------------+--------------+------------------------+
    | backend directory                    | namespace id | url prefix             |
    +======================================+==============+========================+
    | ``myproject/backends/auth``          | ``auth``     | ``/api/auth``          |
    +--------------------------------------+--------------+------------------------+
    | ``myproject/backends/mydomain_v1``   | ``mydomain`` | ``/api/mydomain/v1``   |
    +--------------------------------------+--------------+------------------------+
    | ``myproject/backends/mydomain_v1_2`` | ``mydomain`` | ``/api/mydomain/v1.2`` |
    +--------------------------------------+--------------+------------------------+


A sqlite database is automatically created for each app execution mode: 

.. table:: 
    :align: left

    +--------------------+---------------------------------------------+
    | execution context  | created database                            |
    +====================+=============================================+
    | production mode    | ``backends/mydomain_v1/store/data.db``      |
    +--------------------+---------------------------------------------+
    | development mode   | ``backends/mydomain_v1/store/temp/data.db`` |
    +--------------------+---------------------------------------------+
    | testing mode       | ``:memory:``                                |
    +--------------------+---------------------------------------------+


The ``app.extensions`` module will provide a ``db`` object which permits to:

* model your database without conflict with other database (see :ref:`Modelling Databases`)
* use this database to provide utilities (see :ref:`Using database inside utils`)
* use this database to provide an api (see :ref:`Using database inside api`)
* use this database inside frontends (see :ref:`Using database inside frontends`)

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
    | model class | backend name | ``__tablename__``      | ``__bind_key__``  |
    +=============+==============+========================+===================+
    | ``Item``    | MyDomain 1.0 | ``mydomain_v1_0_item`` | ``mydomain_v1_0`` |
    +-------------+--------------+------------------------+-------------------+
    | ``Item``    | MyDomain 1.5 | ``mydomain_v1_5_item`` | ``mydomain_v1_5`` |
    +-------------+--------------+------------------------+-------------------+
    | ``Post``    | MyDomain 2.0 | ``mydomain_v1_0_post`` | ``mydomain_v2_0`` |
    +-------------+--------------+------------------------+-------------------+


.. DANGER::
    To avoid conflict between databases 
    from different versions of the same backend,
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




Using database inside frontends
-------------------------------

