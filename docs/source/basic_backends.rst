

Creating backend
================

Any backend must have a **domain name** and a **version number**.


``create-backend`` command
--------------------------

To create a ``MyDomain 1.0`` backend, navigate to ``backends`` directory:

.. code-block:: bash

    cd myproject/backends


Then use the command ``create-backend``:

.. code-block:: bash

    pigal create-backend MyDomain 1.0



Default backend structure
--------------------------

This command will create the following structure:

.. code-block::

    /mydomain_v1_0 
    |
    |-- /store            # domain file store
    |   |-- data.db       # domain database
    |
    |-- __init__.py       # backend initialization
    |-- models.py         # database models
    |-- routes.py         # domain Rest API
    |-- utils.py          # domain utilities



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
    | ``myproject/backends/mydomain_v1_0`` | ``mydomain`` | ``/api/mydomain/v1.0`` |
    +--------------------------------------+--------------+------------------------+
    | ``myproject/backends/mydomain_v1_2`` | ``mydomain`` | ``/api/mydomain/v1.2`` |
    +--------------------------------------+--------------+------------------------+

Running backend
---------------

Run project and go to:

* http://127.0.0.1:5000/api to see and test default API with `Swagger UI`_.
* http://127.0.0.1:5000/api/mydomain/v1.0/ping to see the default API results.

.. _Swagger UI: https://swagger.io/tools/swagger-ui/


Customizing backends
---------------------

With this backend structure, you can then:

* create custom reusable functions inside ``utils.py`` file
* create custom Rest API inside ``routes.py`` file (see `Flask-Restx documentation`_)
* create and use databases models inside ``models.py`` file (see :ref:`Creating databases`)

.. _Flask-Restx documentation: https://flask-wtf.readthedocs.io/en/1.2.x/


**Next step in quickstart** : :ref:`Creating databases`