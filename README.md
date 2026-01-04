# Pigal-Flask

Pigal-Flask is an Flask extension which facilitates the creation and management of Pigal projects. 
A **Pigal project** is a modular web portal for an organisation which need to build progressively an integrated information system.
**Pigal** means in french ("Portail d'information et de gestion des activites en ligne").

![SVG Image](docs/diagrams/pigal_project_architecture.drawio.svg)


A Pigal project follow a modular architecture based on 03 components as shown above:
- **app** which provide global theme, configuration and flask extensions
- **frontends** which provide specific frontend
- **backends** which provide specific backend


## Installation

Use the following command to install `Pigal-Flask` extension:

```bash
pip install Pigal-Flask
```

## Quickstart

### Create minimal project

To create a new project ``MyProject`` with a theme ``MyTheme.zip``, use the following command :

```bash
pigal create-project MyProject C:/MyTheme.zip
```

This will create a pigal project with the following structure:

```
/myproject
|   
|-- /app                  # APP SUB-DIRECTORY
|   |-- /static           # theme static files
|   |-- /templates        # theme jinja templates
|   |-- __init__.py       # app initialization
|   |-- config.py         # app configurations
|   |-- extensions.py     # app flask extensions
|   
|-- /frontends                # FRONTENDS SUB-DIRECTORY
|   |-- /demo             # theme live demo frontend
|   |-- /home             # home frontend 
|   |-- __init__.py       # global frontend initialisation
|   
|-- /backends             # MICROSERVICES SUB-DIRECTORY
|   |-- /auth             # authentification backend
|   |-- __init__.py       # global api initialisation


```

To see and customize the project, navigate to `myproject` directory and run the flask app:

```bash
cd myproject
flask run --debug
```

Go to http://127.0.0.1:5000 to see the default project page.

Go to http://127.0.0.1:5000/api to see the default project Rest API.


### Create minimal frontend

To create `MyDomain` frontend, navigate to `frontends` directory and use `create-frontend` command:

```bash
cd frontends
pigal create-frontend MyDomain
```

This will create the following structure:

```
/frontends
|   
|-- /mydomain             # CREATED PAGES DIRECTORY
|   |-- /static           # domain static files
|   |-- /templates        # jinja templates
|   |   |-- /mydomain     # domain templates
|   |
|   |-- __init__.py       # domain initialization
|   |-- forms.py          # domain WTF-forms
|   |-- routes.py         # domain flask routes


```

> [!IMPORTANT]
> frontend can only be created inside the `frontends` directory

Go to http://127.0.0.1:5000/mydomain to see default `MyDomain` page. 

You can modify this frontend (see [Documentation](#)).


### Create minimal backend

In Pigal project, any backend must have a **domain name** and a **version number**. 
To create `MyDomain 1.0` backend, navigate to `myproject/backends` directory and use `create-backend`command:

```bash
pigal create-backend MyDomain 1.0
```

This will create the following structure:

```
/backends
|   
|-- /mydomain_v1_0        # CREATED SERVICE DIRECTORY
|   |-- /store            # new backend files
|   |-- __init__.py       # backend initialization
|   |-- models.py         # domain database models
|   |-- routes.py         # domain Rest API
|   |-- utils.py          # domain utilities

```

> [!IMPORTANT]
> Service can only be created inside the `backends` directory of a pigal project

Go to http://127.0.0.1:5000/api to see the new MyDomain API. 

you can now create databases, change default API or create utilities for frontends and others backends (see [Documentation](#)).


## Contributions


## Licences

