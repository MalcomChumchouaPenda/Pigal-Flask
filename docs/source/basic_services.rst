

Creating domain services
========================

In Pigal project, any microservice must have 
a **domain name** and a **version number**.
To create a ``mydomain`` microservice, 
use the command ``create-service``
inside ``mysite/services`` directory:

.. code-block:: bash

    pigal create-service mydomain 1.0


.. IMPORTANT::
    Service can only be created inside the ``services`` directory


This command will create the following structure:

.. code-block::

    /services
    |   
    |-- /mydomain_v1_0        # CREATED SERVICE DIRECTORY
    |   |-- /store            # new microservice files
    |   |-- __init__.py       # microservice initialization
    |   |-- models.py         # domain database models
    |   |-- routes.py         # domain Rest API
    |   |-- utils.py          # domain utilities
    |   


Inside ``routes.py``, a minimal REST API
is automatically created like this:

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

    +-----------------------------------+--------------+------------------------+
    | service path                      | namespace id | url prefix             |
    +===================================+==============+========================+
    | ``mysite/services/auth``          | ``auth``     | ``/api/auth``          |
    +-----------------------------------+--------------+------------------------+
    | ``mysite/services/mydomain_v1``   | ``mydomain`` | ``/api/mydomain/v1``   |
    +-----------------------------------+--------------+------------------------+
    | ``mysite/services/mydomain_v1_2`` | ``mydomain`` | ``/api/mydomain/v1.2`` |
    +-----------------------------------+--------------+------------------------+
