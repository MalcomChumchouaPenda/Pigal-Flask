

Databases configurations
========================


Default DB configuration
------------------------

The dedicated database of each ``backend`` has an generated ``URI``:


.. table::
    :align: left

    +---------------------+-----------------------------------------------------------------+
    |  Service id         | URI generated in production mode                                |
    +=====================+=================================================================+
    | ``auth``            | ``sqlite:///D:/myproject/backends/auth/store/data.db``          |
    +---------------------+-----------------------------------------------------------------+
    | ``mydomain_v1_0``   | ``sqlite:///D:/myproject/backends/mydomain_v1_0/store/data.db`` |
    +---------------------+-----------------------------------------------------------------+
    | ``mydomain_v1_2``   | ``sqlite:///D:/myproject/backends/mydomain_v1_2/store/data.db`` |
    +---------------------+-----------------------------------------------------------------+


This ``URI`` is generated automatically using templates defined in ``app/config.py``:

.. code-block:: python

    class Config:
        # ... DEFAULT PARAMETERS

    class ProdConfig:
        # ... OTHER PRODUCTION PARAMETERS
        PIGAL_DB_URI_TEMPLATE = 'sqlite:///{backend_dir}/store/data.db'

    class DevConfig:
        # ... OTHER DEVELOPPEMENT PARAMETERS
        PIGAL_DB_URI_TEMPLATE = 'sqlite:///{backend_dir}/store/temp/data.db'

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
    | ``{backend_name}``  | the name of the database backend                                      |
    +---------------------+-----------------------------------------------------------------------+
    | ``{backend_id}``    | the id of the database backend (id = name + version)                  |
    +---------------------+-----------------------------------------------------------------------+
    | ``{backend_dir}``   | the absolute path of the database backend                             |
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
    | ``sqlite:///D:/somedir/{project_name}.db``             | ``sqlite:///D:/somedir/MyProject.db``                    |
    +--------------------------------------------------------+----------------------------------------------------------+
    | ``sqlite:///D:/somedir/{backend_name}.db``             | ``sqlite:///D:/somedir/MyDomain.db``                     |
    +--------------------------------------------------------+----------------------------------------------------------+
    | ``sqlite:///D:/somedir/fake_data.db``                  | ``sqlite:///D:/somedir/fake.db``                         |
    +--------------------------------------------------------+----------------------------------------------------------+
    | ``sqlite:///{project_dir}/somedir/data.db``            | ``sqlite:///D:/myproject/somedir/data.db``               |
    +--------------------------------------------------------+----------------------------------------------------------+
    | ``sqlite:///{backend_dir}/data.db``                    | ``sqlite:///D:/myproject/backends/mydomain_v1_0/data.db``|
    +--------------------------------------------------------+----------------------------------------------------------+
    | ``mysql+mysqldb://root:1234@localhost/{project_id}``   | ``mysql+mysqldb:///root:1234@localhost/myproject``       |
    +--------------------------------------------------------+----------------------------------------------------------+
    | ``mysql+mysqldb://root:1234@localhost/{backend_id}``   | ``mysql+mysqldb:///root:1234@localhost/mydomain_v1_0``   |
    +--------------------------------------------------------+----------------------------------------------------------+


