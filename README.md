# Pigal-Flask

Pigal-Flask is an Flask extension which facilitates the creation and management of modular web portal for organisations.

**Table of contents:**
1. [Principles](#principles)
2. [Installation](#installation)
3. [Quickstart](#quickstart)
4. [Customization](#customization)
5. [Contributions](#contributions)
6. [Licences](#licences)



## Principles
Pigal-Flask facilitates the development of Pigal project. A Pigal project aims to create an modular web portal for an organisation which need to build progressively an integrated information system. **Pigal** means in french ("**P**ortail d'**i**nformation et de **g**estion des **a**ctivites en **l**igne").

A Pigal project follow a modular architecture based on 03 components:
- *app* which provide home pages, auth services and global theme
- *pages* which provide domain specific frontend or UI
- *services* which provide domain specific backend or API



![SVG Image](docs/diagrams/pigal_project_architecture.drawio.svg){width="50%"; style="display: block; margin: 0 auto" }


## Installation

*---(todo)---*

## Quickstart
A Pigal Project has the minimal following structure:
```

/project
├── /pages                # Front-ends or UIs
├── /services             # Microservices or APIs
├── /app                  # Core App

```

>[!IMPORTANT]
> This structure is required for any Pigal project

We can have 03 types of Pigal Projects:
- Project with pages only (*Pigal Frontend Project*)
- Project with services only (*Pigal Backend Project*)
- Project with pages and services (*Pigal Full Project*)

To create any project, we must then:
- create app (*required* steps)
- create pages (*optional* steps)
- create services (*optional* steps)


### Create minimal app (core)

A core `app` has the following minimal structure:

```
/app 
├── __init__.py        # Flask App factory module
├── config.py          # Flask App configurations
├── extensions.py      # Flask extensions initialization

```

Lets define project configuration in `app/config.py`.

```python

class Config:
    PIGAL_ROOT_DIR = '.'
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

Now we can create pages in `pages` directory. Each page has the following minimal structure:
```

/page                # A page directory
├── /static          # Static files (Flask directory)
├── /templates       # Jinja Templates (Flask directory)
├── routes.py        # Page routing (Flask Blueprint)

```

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

Now, we can do for example:

```python

from app.extensions import db
from services.persons_v0.models import Person

person1 = Person(id=1, name='Demo A')
person2 = Person(id=2, name='Demo B')
db.session.add_all([person1, person2])
db.session.commit()

query = db.session.query(Person)
print(query.all())

```

## Contributions


## Licences

