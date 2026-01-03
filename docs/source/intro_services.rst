
Creating domain microservice
============================

Use the following commands to create a microservice inside 
``/<project-name>/services`` directory:

.. code-block:: bash

    pigal create-service <domain> <version>


This will create the following structure:

.. code-block::

    /services
    |   
    |-- /<service_name>       # CREATED SERVICE DIRECTORY
    |   |-- /store            # new microservice files
    |   |-- __init__.py       # microservice initialization
    |   |-- models.py         # domain database models
    |   |-- routes.py         # domain Rest API
    |   |-- utils.py          # domain utilities
    |   


.. IMPORTANT::
    Service can only be created inside the ``/services`` 
    directory of a pigal project
