

Databases configurations
========================


Default DB configuration
------------------------

The dedicated database of each ``service`` has an generated ``URI``:


.. table::
    :align: left

    +---------------------+-----------------------------------------------------------------+
    |  Service id         | URI generated in production mode                                |
    +=====================+=================================================================+
    | ``auth``            | ``sqlite:///D:/myproject/services/auth/store/data.db``          |
    +---------------------+-----------------------------------------------------------------+
    | ``mydomain_v1``     | ``sqlite:///D:/myproject/services/mydomain_v1/store/data.db``   |
    +---------------------+-----------------------------------------------------------------+
    | ``mydomain_v1_2``   | ``sqlite:///D:/myproject/services/mydomain_v1_2/store/data.db`` |
    +---------------------+-----------------------------------------------------------------+


This ``URI`` is generated automatically using templates defined in ``app/config.py``:

.. code-block:: python

    class Config:
        # ... DEFAULT PARAMETERS

    class ProdConfig:
        # ... OTHER PRODUCTION PARAMETERS
        PIGAL_DB_URI_TEMPLATE = 'sqlite:///{service_dir}/store/data.db'

    class DevConfig:
        # ... OTHER DEVELOPPEMENT PARAMETERS
        PIGAL_DB_URI_TEMPLATE = 'sqlite:///{service_dir}/store/temp/data.db'

    class TestConfig:
        # ... OTHER TESTING PARAMETERS
        PIGAL_DB_URI_TEMPLATE = 'sqlite:///:memory:'



Customizing DB URI template
---------------------------

The following variables can be used inside ``PIGAL_DB_URI_TEMPLATE``:

.. table::
    :align: left

    +---------------------+-----------------------------------------------------------------------+
    | Variable names      | variable meanings                                                     |
    +=====================+=======================================================================+
    | ``{service_name}``  | the name of the database service                                      |
    +---------------------+-----------------------------------------------------------------------+
    | ``{service_id}``    | the id of the database service (id = name + version)                  |
    +---------------------+-----------------------------------------------------------------------+
    | ``{service_dir}``   | the absolute path of the database service                             |
    +---------------------+-----------------------------------------------------------------------+
    | ``{project_name}``  | the name of the pigal project                                         |
    +---------------------+-----------------------------------------------------------------------+
    | ``{project_id}``    | the id of the pigal project                                           |
    +---------------------+-----------------------------------------------------------------------+
    | ``{project_dir}``   | the absolute path of the pigal project                                |
    +---------------------+-----------------------------------------------------------------------+

So you can customize this ``PIGAL_DB_URI_TEMPLATE``. For examples:

.. table::
    :align: left

    +--------------------------------------------------------+----------------------------------------------------------+
    | URI template                                           | URI generated                                            |
    +========================================================+==========================================================+
    | ``sqlite:///D:/somedir/{service_name}.db``             | ``sqlite:///D:/somedir/MyDomain.db``                     |
    +--------------------------------------------------------+----------------------------------------------------------+
    | ``sqlite:///D:/somedir/{project_name}.db``             | ``sqlite:///D:/somedir/MyProject.db``                    |
    +--------------------------------------------------------+----------------------------------------------------------+
    | ``sqlite:///D:/somedir/fake_data.db``                  | ``sqlite:///D:/somedir/fake.db``                         |
    +--------------------------------------------------------+----------------------------------------------------------+
    | ``sqlite:///{service_dir}/data.db``                    | ``sqlite:///D:/myproject/services/mydomain_v1/data.db``  |
    +--------------------------------------------------------+----------------------------------------------------------+
    | ``sqlite:///{project_dir}/somedir/data.db``            | ``sqlite:///D:/myproject/somedir/data.db``               |
    +--------------------------------------------------------+----------------------------------------------------------+
    | ``mysql+mysqldb://root:1234@localhost/{service_id}``   | ``mysql+mysqldb:///root:1234@localhost/mydomain_v1``     |
    +--------------------------------------------------------+----------------------------------------------------------+
    | ``mysql+mysqldb://root:1234@localhost/{project_id}``   | ``mysql+mysqldb:///root:1234@localhost/myproject``       |
    +--------------------------------------------------------+----------------------------------------------------------+


