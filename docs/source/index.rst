.. Pigal-Flask documentation master file, created by
   sphinx-quickstart on Sun Nov 30 20:04:08 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Pigal-Flask
===========

**Pigal-Flask** is an Flask extension that simplifies developing modular web portals
for organisations building an integrated information systems.

A **Pigal project** is a Flask application with a modular architecture based on 03 components:

* **app** which provide global configuration, extensions and theme
* **frontends** which provide specific domain frontends
* **backends** which provide specific domain backends

.. image:: ../diagrams/pigal_project_architecture.drawio.svg


This architecture provides the following benefits:

* **Easier collaboration**: Frontend and Backend developers can easily collaborate
* **Easier scalability**: Developers can easily add and remove features to projects
* **Easier maintainability**: Projects can easily be maintained, tested and refactored

**Pigal-Flask** allows web developpers to:

* develop and share views, pages and themes
* develop and share services and functionnalities
* develop and manage multiple databases
* quickly add common security mechanisms
* easily implement multi-language support
* enforce best conventions in development teams


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

