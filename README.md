# Pigal-Flask

Pigal-Flask is an extension for Flask to create Pigal Projects


## Quickstart
A Pigal Project has the following structure:
```

/project
├── /pages                # Front-ends or UIs
├── /services             # Microservices or APIs
├── app.py                # Main entry point

```

We can have 03 types of Pigal Projects:
- Project with pages only (*Pigal Frontend Project*)
- Project with services only (*Pigal Backend Project*)
- Project with pages and services (*Pigal Full Project*)


### Minimal Pigal Frontend Project

We must create and initialize a *Pigal extension*

```python
from pigal_flask import Pigal

class Config:
    PIGAL_ROOT_DIR = '.'

app = Flask(__name__)
app.config.from_object(Config)
pigal = Pigal(app)

```

Then we can implement pages. each page has the following minimal structure:
```

/page                # A page directory
├── /static          # Static files (Flask standard directory)
├── /templates       # Jinja Templates (Flask standard directory)
├── routes.py        # Page routing (Flask Blueprint)

```

To create a *page*, we must create a `PigalUi` instance in `routes.py`.

```python
from pigal_flask import PigalUi

ui = PigalUi(__file__)

@ui.route('/')
def index():
    return "Hello Word"

```

A `PigalUi` is a extended Flask Blueprint whose `name` and `url_prefix` are automatically created. 

For examples:

| Page name  | Blueprint name |Url prefix  |
| ---        | ---            | ---        |
| `payments` | `payments`     | `/payments`|
| `students` | `students`     |`/students` |
| `home`     | `home`         |`/`         |


Some examples with `home` and `students` blueprints:

```html

<body>
    <a href="{{ url_for('home.index') }}">home index page</a>
    <a href="{{ url_for('home.some') }}">home some page</a>
    <a href="{{ url_for('students.some') }}">students some page</a>
</body>
```

> [!IMPORTANT]
> An *home page* provide the special index *page* required by any *pigal frontend* project

> [!NOTE]
> `PigalUi` instances which are in *routes* module are automatically discovered and registered by *Pigal* instance.


### Minimal Pigal Backend Project

As for *Pigal Frontend*, we must create and initialize an *Pigal extension*

```python

# ... imports ...

class Config:
    PIGAL_ROOT_DIR = '.'
    PIGAL_API_VERSION = '1.0'

app = Flask(__name__)
app.config.from_object(Config)
pigal = Pigal(app)

```

A *service* has the following minimal structure:

```

/service             # A page directory
├── /store           # data store (required directory)
├── routes.py        # Service routing (Flask-Restx Api/Namespace)

```

To create a *service*, we must create a `PigalApi` instance in `routes.py`.

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
> `PigalApi` instances which are in *routes* module are automatically discovered and registered by *Pigal* instance.

A `PigalApi` is a extended Flask-Restx `Namespace` whose `name` and `url_prefix` are automatically created. 

For examples:

| Service name  | Namespace id | Url prefix         |
| ---           | ---          | ---                |
| `payments_v0` | `payments`   | `/api/payments/v0` |
| `students_v2` | `students`   | `/api/students/v2` |


### Minimal Pigal Full Project (to do)


## Database management

To create database, you must have the minimal following structure:

```

/service             # A page directory
├── routes.py        # Service routing (Flask-Restx Api/Namespace)
├── models.py        # Database modelling (Flask-SqlAlchemy Model)
├── ...

```

> [!IMPORTANT]
> All database must be defined in services.

In `app/config.py` create a configuration where you specify a template for database URI. For example, we use a template wich use `root_dir` and `service_id` variables to create a `sqlite` database URI:

```python

class Config:
    # ... other configs 
    PIGAL_DB_URI_TEMPLATE = 'sqlite:///{root_dir}/{service_id}.db'

```

In `app/extensions.py` create a `PigalDb` extension:

```python

from pigal_flask import Pigal, PigalDb

db = PigalDb()
pigal = Pigal()
# ... others extensions

```
With `db` you can define models in any `models.py` like this:

```python

from app.extensions import db

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

```

now in `app/__init__.py` initialize created `PigalDb` instance with your `app` instance:

```python

from flask import Flask
from .extensions import db, pigal
from .config import Config

app = Flask(__name__)
app.config.from_object(Config) # configure app
db.init_app(app)               # init db extension
pigal.init_app(app)            # init pigal extension

with app.app_context():
    db.create_all()            # create all tables

```


A `PigalDb` is a subclass of `SQLAlchemy` provided by *Flask-SQLAlchemy*. For example, with a service `demo_v0`, we can do:

```python

from app.extensions import db
from services.demo_v0.models import Person

person1 = Person(id=1, name='Demo A')
person2 = Person(id=2, name='Demo B')
db.session.add_all([person1, person2])
db.session.commit()

query = db.session.query(Person)
print(query.all())

```