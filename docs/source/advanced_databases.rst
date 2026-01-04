

Databases configurations
========================

The dedicated database of each ``service`` has an generated ``URI``.
This ``URI`` is generated automatically using template 
defined in ``app/config.py``:

.. code-block:: python

    class Config:

        PIGAL_DB_URI_TEMPLATE = 'sqlite:///{service_dir}/store/data.db'
        # ... other parameters


The following variables can be used inside ``PIGAL_DB_URI_TEMPLATE``:

.. table::
    :align: left

    +---------------------+------------------------------------------------------------------------------+
    | Variable names      | variable meanings                                                            |
    +=====================+==============================================================================+
    | ``{service_name}``  | the name of the database service                                             |
    +---------------------+------------------------------------------------------------------------------+
    | ``{service_id}``    | the id of the database service (id = name + version)                         |
    +---------------------+------------------------------------------------------------------------------+
    | ``{service_dir}``   | the absolute path of the database service                                    |
    +---------------------+------------------------------------------------------------------------------+
    | ``{project_id}``    | the id of the pigal project                                                  |
    +---------------------+------------------------------------------------------------------------------+
    | ``{project_dir}``   | the absolute path of the pigal project                                       |
    +---------------------+------------------------------------------------------------------------------+

So you can customize this ``PIGAL_DB_URI_TEMPLATE``. For examples:

.. table::
    :align: left

    +-----------------------------------------------------------+-----------------------------------------------------------+
    | URI template                                              | URI generated                                             |
    +===========================================================+===========================================================+
    | ``sqlite:///D:/somedata/{service_name}.db``               | ``sqlite:///D:/somedata/mydomain.db``                     |
    +-----------------------------------------------------------+-----------------------------------------------------------+
    | ``sqlite:///{service_dir}/data.db``                       | ``sqlite:///D:/mysite/services/mydomain_v1/data.db``      |
    +-----------------------------------------------------------+-----------------------------------------------------------+
    | ``sqlite:///{project_dir}/somedir/data.db``               | ``sqlite:///D:/mysite/somedir/data.db``                   |
    +-----------------------------------------------------------+-----------------------------------------------------------+
    | ``mysql+mysqldb://root:1234@localhost/{service_id}``      | ``mysql+mysqldb:///root:1234@localhost/mydomain_v1``      |
    +-----------------------------------------------------------+-----------------------------------------------------------+
    | ``mysql+mysqldb://root:1234@localhost/{project_id}``      | ``mysql+mysqldb:///root:1234@localhost/mysite``           |
    +-----------------------------------------------------------+-----------------------------------------------------------+


