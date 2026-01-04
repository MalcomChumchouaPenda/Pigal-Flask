
Adding new extensions
=====================


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
        PIGAL_PROJECT_NAME = 'demo'
        PIGAL_PROJECT_VERSION = '1.0'


we can modify to add parameters of new extensions:

.. code-block:: python

    class Config:

        # ... other parameters
        FOO_PARAMS1 = 'a1'
        BAR_PARAMS1 = 'b1'
        BAR_PARAMS2 = 'b2'


Initialize extension with App
-----------------------------

by default ``app/__init__.py`` contains the following code:

.. code-block:: python

    from flask import Flask
    from .extensions import db, pigal
    from .config import Config


    # create Flask app
    app = Flask(__name__)
    app.config.from_object(Config)

    # initialize Flask extensions
    db.init_app(app)
    pigal.init_app(app)

    # create all databases tables
    with app.app_context():
        db.create_all()            



finally, we must modify this file, to initialize new extensions:


.. code-block:: python

    # ... default imports
    from .extensions import foo, bar

    # ... previous initialisation process
    foo.init_app(app)
    bar.init_app(app)
    
