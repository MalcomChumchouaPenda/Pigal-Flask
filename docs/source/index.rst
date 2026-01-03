.. Pigal-Flask documentation master file, created by
   sphinx-quickstart on Sun Nov 30 20:04:08 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Pigal-Flask documentation
=========================

Pigal-Flask is an Flask extension which facilitates the development of Pigal projects.
A **Pigal project** is a modular web portal for an organisation. 
This will help an organisation to build progressively an integrated information system. 
**Pigal** means in french ("Portail d'information et de gestion des activites en ligne").

.. image:: ../diagrams/pigal_project_architecture.drawio.svg

A Pigal project follow a modular architecture based on 03 components as shown above:

* **app** which provide global Flask configuration, extensions and theme
* **pages** which provide specific frontends or UI (User Interface)
* **services** which provide specific backends or API (Application Programming Interface)

The rest of this documentation will help you to use Pigal-Flask...


Installation
------------

Use the following command to install ``Pigal-Flask`` extension:

.. code-block:: bash

    pip install Pigal-Flask


User Guide
----------

.. toctree::
   :maxdepth: 2

   intro
   tuto
   api 


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

