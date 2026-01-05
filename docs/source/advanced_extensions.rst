
Adding flask extensions
=======================


You can improve a pigal project, you can add new Flask extensions by:

* installing the choosen extension
* creating the extension
* configuring the extension in app
* initializing the extension with app


To illustrate this, we suppose that 
we have to add two flask-extension to the ``myproject``:

* ``Foo`` extension from ``flask_foo``
* ``Bar`` extension from ``flask_bar``


Install new extension
---------------------


Creating extension
------------------


By default, ``app/extensions.py`` contains the following code:

.. code-block:: python

    from pigal_flask import Pigal, PigalDb

    db = PigalDb()
    pigal = Pigal()


We must modify this file to create installed extensions:

.. code-block:: python

    # ... other imports 
    from flask_foo import Foo
    from flask_bar import Bar

    # ... other extensions
    foo = Foo()
    bar = Bar()


Configure extension in App
---------------------------

by default, ``app/config.py`` contains the following code:

.. code-block:: python

    class Config:
        PIGAL_PROJECT_NAME = 'MyProject'
        PIGAL_THEME_UI_SYSTEM = 'MyUISystem'
        PIGAL_THEME_LIVE_DEMO = True

    # ... OTHER CONFIG CLASSES


we can modify to add parameters of new extensions:

.. code-block:: python

    class Config:
        # ... PREVIOUS PARAMETERS
        FOO_PARAMETER = 'foo_option'
        BAR_PARAMETER = 'bar_option'

    # ... OTHER CONFIG CLASSES


Initialize extension with App
-----------------------------

by default ``app/__init__.py`` contains the following code:

.. code-block:: python

    from flask import Flask
    from .extensions import db, pigal
    from .config import Config


    def create_app():
        app = Flask(__name__)
        app.config.from_object(Config)

        db.init_app(app)         # initialize PigalDb extension
        pigal.init_app(app)      # initialize Pigal extension

        with app.app_context():
            db.create_all()      # create all databases tables           



finally, we must modify this file, to initialize new extensions:


.. code-block:: python

    # ... default imports
    from .extensions import foo, bar

    # ... previous initialisation process
    foo.init_app(app)
    bar.init_app(app)
    
