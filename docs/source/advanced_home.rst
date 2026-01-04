

Customizing home pages
======================


Default home structure
----------------------

``home`` pages has similar structure as other domain pages:

.. code-block::

    /home            
    |-- /static                     # static files
    |-- /templates                  # jinja templates
    |   |-- /home                   # home templates
    |       |-- dashboard.jinja     # home dashboard template
    |       |-- index.jinja         # home index template
    |       |-- login.jinja         # home login template
    |
    |-- __init__.py                 # home initialization
    |-- forms.py                    # home WTF-forms
    |-- routes.py                   # home routing
    |   

But, the ``home`` pages must provides 04 specific routes with 5 roles:

.. table::
    :align: left

    +--------------------+----------------+--------------+--------------------------------+
    | UI routes          | Default urls   | HTTP methods | UI Roles                       |
    +====================+================+==============+================================+
    | ``home.index``     | ``/``          | ``GET``      | Display landing home page      |
    +--------------------+----------------+--------------+--------------------------------+
    | ``home.dashboard`` | ``/dashboard`` | ``GET``      | Display dashboard home page    |
    +--------------------+----------------+--------------+--------------------------------+
    | ``home.login``     | ``/login``     | ``GET``      | Display login form page        |
    +--------------------+----------------+--------------+--------------------------------+
    | ``home.login``     | ``/login``     | ``POST``     | Handle login form submission   |
    +--------------------+----------------+--------------+--------------------------------+
    | ``home.logout``    | ``/logout``    | ``POST``     | Handle logout process          |
    +--------------------+----------------+--------------+--------------------------------+


By default, ``home/routes.py`` provides this roles and routes:

.. code-block:: python

    from flask import render_template, redirect, url_for
    from flask_login import login_user, logout_user
    from pigal_flask import PigalUi
    from .forms import LoginForm
    from services.auth.models import User


    ui = PigalUi(__file__)


    @ui.route('/')
    def index():
        return render_template('home/index.jinja')
        
    @ui.route('/dashboard')
    @ui.login_required
    def dashboard():
        return render_template('home/dashboard.jinja')


    @ui.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            userid = form.userid.data
            user = User.query.filter_by(id=userid).first()
            if user and user.password == form.password.data:
                login_user(user)
            return redirect(url_for('home.dashboard'))
        return render_template('home/login.jinja')
        
    @ui.route('/logout', methods=['POST'])
    def logout():
        logout_user()
        return redirect(url_for('home.index'))


``home/forms.py`` provide by default a ``LoginForm`` class:

.. code-block:: python

    from flask_wtf import FlaskForm
    from wtforms import StringField, PasswordField
    from wtforms.validators import DataRequired


    class LoginForm(FlaskForm):
        userid = StringField("User ID", validators=[DataRequired()])
        password = PasswordField("Password", validators=[DataRequired()])


Adding or editing home views
----------------------------

So, you can customize this default ``home`` by adding or editing:

* flask routes inside ``routes.py`` to modify navigation
* jinja templates inside ``templates/home`` to modify page contents
* flask forms inside ``forms.py`` to modify user input validation 



Deleting home views
-------------------

However, unlike usual pages, in ``home`` pages you shall not remove:

* required routes: ``index``, ``dashboard``, ``login`` and ``logout``
* required templates: ``index.jinja``, ``login.jinja`` and ``dashboard.jinja``


