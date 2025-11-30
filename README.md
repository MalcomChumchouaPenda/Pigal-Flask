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

We must create and initialize an app with Pigal extension

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

/page                      # A page directory
├── /static                # Static files (Flask standard directory)
├── /templates             # Jinja Templates (Flask standard directory)
├── routes.py              # Page routing (Flask Blueprint)

```

To create a page, we must create a *PigalUi* instance in *routes.py*.

```python
from pigal_flask import PigalUi

ui = PigalUi(__name__)

@ui.route('/')
def index():
    return "Hello Word"

```

A *PigalUi* is a extended Flask Blueprint. It is automatically discovered and registered by *pigal* into Flask App. The name of the blueprint and its url prefix is automatically created based on page name. 

For examples:

| Page name | Blueprint name | Url prefix |
| ---       | ---            | ---        |
| payments  | *payments*     |*/payments* |
| students  | *students*     |*/students* |
| home      | *home*         |*/*         |


**NB**: The *home* page is the special root page


### Minimal Pigal Backend Project (to do)


### Minimal Pigal Full Project (to do)

