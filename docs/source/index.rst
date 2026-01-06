.. Pigal-Flask documentation master file, created by
   sphinx-quickstart on Sun Nov 30 20:04:08 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Pigal-Flask
===========

**Pigal-Flask** is a Flask extension that simplifies the development of **Pigal projects**. 
Pigal projects are **modular web portals** that facilitate the management of online information and activities.
Pigal-Flask helps web developpers to collaborate using conventions and best practices.


Basic Concepts
--------------

A **Pigal project** is a Flask application with a modular architecture based on 03 components:

* **app** which provide global configuration, extensions and theme
* **frontends** which provide specific domain frontends
* **backends** which provide specific domain backends

.. image:: ../diagrams/pigal_project_architecture.drawio.svg


This architecture provides the following benefits:

* **Easier collaboration**: Frontend and Backend developers can easily collaborate
* **Easier scalability**: Developers can easily add and remove features to projects
* **Easier maintainability**: Projects can easily be maintained, tested and refactored


The development of Pigal project is based on three project types:

* **template projects** offer a reusable foundation and pre-configured structure to start new projects
* **module projects** are customized from templates projects to address specific business domains
* **application projects** integrate multiple modules projects to form a complete web application


.. image:: ../diagrams/pigal_development_cycle.drawio.svg


In this cycle, template, module or application projects contain:

* **demo apps**, **frontends** and **backends** which showcase examples and tutorials
* **org apps**, **frontends** and **backends** which implement real business functionnality

So application projects are built by assembling multiple module projects created from template projects:

* **full-stack developers** can create and share template project
* **frontend developpers** will create frontends in module projects
* **backend developpers** will create backends in module projects
* **project managers** can finally assemble these module into application projects



Installation
------------

Use the following command to install ``Pigal-Flask`` extension:

.. code-block:: bash

    pip install Pigal-Flask



User Guide
----------

.. toctree::
   :maxdepth: 2

   basic
   advanced
   api


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

