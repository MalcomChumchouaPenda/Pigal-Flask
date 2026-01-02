# Pigal-Flask

Pigal-Flask is an Flask extension which facilitates the creation and management of Pigal projects. A **Pigal project** is a modular web portal for an organisation which need to build progressively an integrated information system.
**Pigal** means in french ("Portail d'information et de gestion des activites en ligne").

![SVG Image](docs/diagrams/pigal_project_architecture.drawio.svg)


A Pigal project follow a modular architecture based on 03 components as shown above:
- **app** which provide global theme, configuration and flask extensions
- **pages** which provide domain specific frontend or UI (User Interface)
- **services** which provide domain specific backend or API (Application Programming Interface)


## Installation

Use the following command to install `Pigal-Flask` extension:

```bash
pip install Pigal-Flask
```

## Quickstart

### Create minimal project

Use the following command to create a new pigal project:

```bash
pigal create-project <my-project> <my-theme>
```

This will create a pigal project with the following structure:

```
/<my-project>
│   
├── /app                  # core app
│   ├── /static           # theme static files
│   ├── /templates        # theme jinja templates
│   ├── __init__.py       # app initialization
│   ├── config.py         # app configurations
│   ├── extensions.py     # app flask extensions
│   
├── /pages                # front-ends or UIs
│   ├── /home             # home front-end or UI
│   ├── __init__.py       # global UI initialisation
│   
├── /services             # microservices or APIs
│   ├── /auth             # Authentification microservice
│   ├── __init__.py       # global API initialisation
│   

```

### Create minimal pages

Use the following commands to create domain specific pages inside pages:

```bash
cd <my-project>/pages
pigal create-pages <my-domain>
```

This will create the following structure:

```
/pages
│   
├── /<my-domain>          # domain pages
│   ├── /static           # domain static files
│   ├── /templates        # domain jinja templates
│   ├── __init__.py       # domain initialization
│   ├── forms.py          # domain WTF-forms
│   ├── routes.py         # domain flask routes
│   

```

> [!IMPORTANT]
> pages can only be created inside the `pages` directory of a pigal project


### Create minimal services

Use the following commands to create a microservice inside services directory:

```bash
cd <my-project>/services
pigal create-service <my-domain> <my-version>
```

This will create the following structure:

```
/services
│   
├── /<service_name>       # new microservice
│   ├── /store            # new microservice files
│   ├── __init__.py       # microservice initialization
│   ├── models.py         # domain database models
│   ├── routes.py         # domain Rest API
│   ├── utils.py          # domain utilities
│   

```

> [!IMPORTANT]
> Service can only be created inside the `services` directory of a pigal project




### Create minimal app (core)



Lets define project configuration in `app/config.py`.

```python

class Config:
    PIGAL_PROJECT_NAME = 'Demo'
    PIGAL_PROJECT_VERSION = '1.0'

```

Lets create `Pigal` extension in `app/extensions.py`.

```python

from pigal_flask import Pigal, PigalDb

pigal = Pigal()

```

Finally in `app/__init__.py`, create Flask `app` :

```python

from flask import Flask
from .extensions import db, pigal
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)  # configure app
pigal.init_app(app)             # init pigal extension

```

### Create minimal page (frontend)


To create a page, we must create a `PigalUi` instance in its `routes.py`. For example, for a `demo` page, we can write in `pages/demo/routes.py`:

```python
from pigal_flask import PigalUi

ui = PigalUi(__file__)

@ui.route('/')
def index():
    return "Hello Word"

```

A `PigalUi` is a extended Flask Blueprint whose `name` and `url_prefix` are automatically created. For examples:

| page name  | blueprint name | url prefix  |
| ---        | ---            | ---         |
| `payments` | `payments`     | `/payments` |
| `students` | `students`     | `/students` |


Some examples with `payments` and `students` blueprints:

```html

<body>
    <a href="{{ url_for('payments.index') }}">payments index page</a>
    <a href="{{ url_for('payments.some') }}">payments some page</a>
    <a href="{{ url_for('students.some') }}">students some page</a>
</body>
```

> [!NOTE]
> `ui` objects which are in any `pages/<page_id>/routes.py` module are automatically discovered and registered by `Pigal` extension.

> [!IMPORTANT]
> To avoid conflict with others pages templates, in each we must identify its specific templates either by creating a directory or by using prefix

Examples of templates organisation with **Page Template Directory**:

```
/pages
├── /payments                  # Payments page directory
│   ├── /templates             # Jinja Templates
│   │   ├── /payments          # Page Template Directory
│   │   │   ├── page1.html
│   │   │   ├── page2.html
│   │   │   ├── page3.html
│   ...
```

Examples of templates organisation with **Page Template Prefix**:

```
/pages
├── /payments                    # Payments page directory
│   ├── /templates               # Jinja Templates with Page Prefix
│   │   ├── payments-page1.html
│   │   │── payments-page2.html
│   │   │── payments-page3.html
│   ...
```



### Create minimal service (backend)

We can create services in `services` directory. Each service has the following minimal structure:

```

/service             # A service directory
├── /store           # Data store (Pigal directory)
├── routes.py        # Service routing (Flask-Restx Namespace)

```

To create a service, we must create a `PigalApi` instance in its `routes.py`. For example, for a `demo_v0` service, we can write in `services/demo_v0/routes.py`:

```python

from flask_restx import Resource
from pigal_flask import PigalApi

api = PigalApi(__file__)

@api.route('/hello')
class HelloApi(Resource):
    def get(self):
        return {'message':'Hello World'}

```

> [!NOTE]
> `api` objects which are in any `services/<service_id>/routes.py` module are automatically discovered and registered by `Pigal` instance.

A `PigalApi` is a extended Flask-Restx `Namespace` whose `name` and `url_prefix` are automatically created. For examples:

| service name  | namespace id | url prefix         |
| ---           | ---          | ---                |
| `payments_v0` | `payments`   | `/api/payments/v0` |
| `students_v2` | `students`   | `/api/students/v2` |


## Customization

### Create minimal database

Before creating any database, we must first specify a template for database URI in `app/config.py`:

```python

class Config:
    # ... other constants
    PIGAL_DB_URI_TEMPLATE = 'sqlite:///{root_dir}/{service_id}.db'

```

> [!NOTE]
> In the previous example, we use a template which use `root_dir` and `service_id` variables to create a `sqlite` database URI.

Then, in `app/extensions.py` create a `PigalDb` extension:

```python

from pigal_flask import Pigal, PigalDb

db = PigalDb()
pigal = Pigal()
# ... others extensions

```

Finally in `app/__init__.py` file, init `PigalDb` instance with `app` and create tables:

```python

from flask import Flask
from .extensions import pigal, db
from .config import Config

app = Flask(__name__)
app.config.from_object(Config) # configure app
db.init_app(app)               # init db extension
pigal.init_app(app)            # init pigal extension

with app.app_context():
    db.create_all()            # create all tables

```

Now we can create *database*. each *database* is created inside one *service*. A *service* with *database* must have a `models.py` file:

```
/service             
├── /store           # Data store (Pigal directory)
├── routes.py        # Service routing (Flask-Restx Namespace)
├── models.py        # Database modelling (Flask-SqlAlchemy Model)
├── ...   

```

With `db` you can define models in any `models.py`. This is an example of model in `services/persons_v0/models.py`:

```python

from app.extensions import db

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

```

> [!IMPORTANT]
> A `PigalDb` is a subclass of `SQLAlchemy` provided by *Flask-SQLAlchemy*.

Now, in `services/persons_v0/routes.py` for example, we can create an api and model:

```python

from flask_restx import Resource, fields
from pigal_flask import PigalApi
from app.extensions import db
from services.persons_v0.models import Person

api = PigalApi(__file__)

person_model = api.model('Person', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True)
})
```

> [!NOTE]
> `PigalApi` will automatically prefix marshall `Model.name` to avoid conflict between models created inside differents versions of the same service. In the example above, the name of `person_model` will be `persons_v0.Person` instead of `Person`

Then in `services/persons_v0/routes.py`, we can create CRUD routes for `Person`:

```python

# ...

@api.route('/persons')
class PersonsApi(Resource):

    @api.marshal_list_with(person_model)
    def get(self):
        '''list all persons'''
        return Person.query.all()
    
    @api.expect(person_model)
    @api.marshal_with(person_model)
    def post(self):
        '''add new person'''
        data = api.payload
        new_person = Person(name=data['name'])
        db.session.add(new_person)
        db.session.commit()
        return new_person

```


### Create minimal home page

A real app need a home UI (*User Interface*). This is done by creating a `home` page in `/app` directory. This `home` page has the same minimal structure than any page in Pigal-Flask:

```
/app
├── /home                # Home page directory
│   ├── /static          # Static files (Flask directory)
│   ├── /templates       # Jinja Templates (Flask directory)
│   ├── routes.py        # Page routing (Flask Blueprint)
│   ...
```

The `home` page must provides 04 required UI:

| blueprint routes | urls         | methods | roles                          |
| ---------------- | ------------ | ------- | ------------------------------ |
| `home.index`     | `/`          | `GET`   | Display landing home page      |
| `home.dashboard` | `/dashboard` | `GET`   | Display dashboard home page    |
| `home.login`     | `/login`     | `GET`   | Display login form page        |
| `home.login`     | `/login`     | `POST`  | Handle login form submission   |
| `home.logout`    | `/logout`    | `POST`  | Handling logout process        |


So, as for any page, we must create `PigalUi` instance and routes in `app/home/routes.py`. For example, we can write:

```python
from flask import render_template, redirect
from pigal_flask import PigalUi

ui = PigalUi(__file__)

@ui.route('/')
def index():
    return render_template('home-index.html')
    
@ui.route('/dashboard')
def dashboard():
    return render_template('home-dashboard.html')

@ui.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # ... authentification
        return redirect(url_for('home.dashboard'))
    return render_template('home-login.html')
    
@ui.route('/logout', methods=['POST'])
def logout():
    # ... logout
    return redirect(url_for('home.index'))

```



## Contributions


## Licences

