
Adding new extensions
=====================

There are a couple of ways to improve or extend:

1. add new flask extensions to add new functionnalities
2. change App configurations for testing, development or production

So how would you then actually implement that?

To illustrate this, we suppose that 
we have created a project called ``demo``.
This project will contain ``/app`` directory with the following files:

* ``config.py``
* ``extensions.py``
* ``__init__.py``


The ``config.py`` contains the following code:

.. code-block:: python

    class Config:
        PIGAL_PROJECT_NAME = 'demo'
        PIGAL_PROJECT_VERSION = '1.0'


The ``extensions.py`` contains the following code:

.. code-block:: python

    from pigal_flask import Pigal, PigalDb

    db = PigalDb()
    pigal = Pigal()


The ``__init__.py`` contains the following code:

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


To illustrate this, we suppose that 
we have to add two flask-extension to the ``demo`` project:

* ``Foo`` extension from ``flask_foo``
* ``Bar`` extension from ``flask_bar``


To do this, we must modify first the ``extensions.py`` 
by adding following codes:

.. code-block:: python

    # ... other imports 
    from flask_foo import Foo
    from flask_bar import Bar

    # ... other extensions
    foo = Foo()
    bar = Bar()
    


Then, if necessary we will modify the ``config.py`` 
by adding following codes:

.. code-block:: python

    class Config:

        # ... other parameters
        FOO_PARAMS1 = 'a1'
        BAR_PARAMS1 = 'b1'
        BAR_PARAMS2 = 'b2'


finally, we must modify the ``__init__.py``
by adding following codes:


.. code-block:: python

    # ... default imports
    from .extensions import foo, bar

    # ... previous initialisation process
    foo.init_app(app)
    bar.init_app(app)
    
