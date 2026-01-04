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

Use the following command to create a new pigal project ``mysite`` with a theme ``mytheme.zip``:

```bash
pigal create-project mysite C:/mytheme.zip
```

This will create a pigal project with the following structure:

```
/mysite
|   
|-- /app                  # APP SUB-DIRECTORY
|   |-- /static           # theme static files
|   |-- /templates        # theme jinja templates
|   |-- __init__.py       # app initialization
|   |-- config.py         # app configurations
|   |-- extensions.py     # app flask extensions
|   
|-- /pages                # FRONTENDS SUB-DIRECTORY
|   |-- /demo             # theme live demo frontend
|   |-- /home             # home frontend 
|   |-- __init__.py       # global frontend initialisation
|   
|-- /services             # MICROSERVICES SUB-DIRECTORY
|   |-- /auth             # authentification microservice
|   |-- __init__.py       # global api initialisation
|   

```

You can now run the Flask App to see the project in `debug` mode:

```bash
flask run --debug
```

Go to http://127.0.0.1:5000 to see the default pages of the project. Go to http://127.0.0.1:5000/api to see the default API of the project.


### Create minimal pages

To create specific pages related to `mydomain`, use the following commands inside `mysite/pages`:

```bash
pigal create-pages mydomain
```

This will create the following structure:

```
/pages
|   
|-- /mydomain             # CREATED PAGES DIRECTORY
|   |-- /static           # domain static files
|   |-- /templates        # domain jinja templates
|   |   |-- /mydomain     # specific pages templates
|   |
|   |-- __init__.py       # domain initialization
|   |-- forms.py          # domain WTF-forms
|   |-- routes.py         # domain flask routes
|   

```

> [!IMPORTANT]
> pages can only be created inside the `pages` directory of a pigal project

Go to http://127.0.0.1:5000/mydomain to see the default mydomain pages. you can modify theses pages (see [Documentation](#)).


### Create minimal services

In Pigal project, any microservice must have 
a **domain name** and a **version number**. Use the following commands to create a microservice ``mydomain 1.0`` inside `mysite/services` directory:

```bash
pigal create-service mydomain 1.0
```

This will create the following structure:

```
/services
|   
|-- /mydomain_v1_0        # CREATED SERVICE DIRECTORY
|   |-- /store            # new microservice files
|   |-- __init__.py       # microservice initialization
|   |-- models.py         # domain database models
|   |-- routes.py         # domain Rest API
|   |-- utils.py          # domain utilities
|   

```

> [!IMPORTANT]
> Service can only be created inside the `services` directory of a pigal project

Go to http://127.0.0.1:5000/api to see the new mydomain API. 

you can now create databases, change default API or create utilities for pages and others services (see [Documentation](#)).


## Contributions


## Licences

