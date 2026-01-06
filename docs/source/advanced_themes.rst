
Theme configurations
====================

Any project must use a theme which can be change or configured:

.. image:: ../diagrams/pigal_ui_system.drawio.svg


The **UI System** define an **abstract sytem** of:

* colors used by themes
* fonts used by themes
* macros required by themes
* layouts required by themes
* blocks used in layouts


A **theme** define **concrete system** of:

* colors predefined
* fonts predefined
* layouts provided to frontend developers
* macros provided to frontend developers
* blocks provided into layouts



Default theme configuration
----------------------------

Theme is configured in ``app/config.py``:

.. code-block:: python

    class Config:
        # ... OTHER DEFAULT PARAMETERS
        PIGAL_THEME_LIVE_DEMO = True
        PIGAL_THEME_UI_SYSTEM = 'xy'
        PIGAL_THEME_NAME = 'MyTheme'

    # ... OTHER CONFIG CLASSES


These parameters allow to:

.. table::
    :align: left

    +----------------------------+--------------------------------------------+
    | Parameters                 | Roles                                      |
    +============================+============================================+
    | ``PIGAL_THEME_LIVE_DEMO``  | enable or disable theme live demo          |
    +----------------------------+--------------------------------------------+
    | ``PIGAL_THEME_UI_SYSTEM``  | get the id of UI system used by theme      |
    +----------------------------+--------------------------------------------+
    | ``PIGAL_THEME_NAME``       | get the name of theme used                 |
    +----------------------------+--------------------------------------------+

.. DANGER::
    You must never edit manually ``PIGAL_THEME_UI_SYSTEM`` and ``PIGAL_THEME_NAME`` parameters

.. NOTE::
    The name of theme zip file has the format ``<theme_name>_<ui_system>.zip``. For examples:
    
    .. table::
        :align: left

        +------------+---------------+------------------------+
        | Theme name | Ui System     | Zip file name          |
        +============+===============+========================+
        | MyTheme    | xy            | ``MyTheme_xy.zip``     |
        +------------+---------------+------------------------+
        | MyTheme    | abc           | ``MyTheme_abc.zip``    |
        +------------+---------------+------------------------+
        | OtherTheme | abc           | ``OtherTheme_abc.zip`` |
        +------------+---------------+------------------------+


Changing theme
--------------

Before changing theme, you must download the new theme (``MyNewTheme_xy.zip`` for example).

To replace ``MyTheme`` theme by ``MyNewTheme``, navigate to ``MyProject`` directory:

.. code-block:: bash

    cd myproject


use ``change-theme`` command:

.. code-block:: bash

    pigal change-theme C:/MyNewTheme_xy.zip


Run the flask app to see the result:

.. code-block:: bash

    flask run


Go to:

* http://127.0.0.1:5000 to see the new project pages.
* http://127.0.0.1:5000/demo to see examples of new theme frontend pages.
* http://127.0.0.1:5000/demo/docs to see documentation page of new theme used.


.. IMPORTANT::
    Any theme can only be replaced by another theme with the **same UI System** !



Removing live demo
------------------

To remove live demo only on production mode, change ``app/config.py``:

.. code-block:: python

    # ... OTHER CONFIG CLASSES

    class ProdConfig:
        # ... OTHER PRODUCTION PARAMETERS
        PIGAL_THEME_LIVE_DEMO = False



To remove live demo, for all execution mode:

.. code-block:: python

    class Config:
        # ... OTHER DEFAULT PARAMETERS
        PIGAL_THEME_LIVE_DEMO = False

    # ... OTHER CONFIG CLASSES

