
Sharing projects
================


Development cycle
-----------------

Any project can contain two type of components:

* **demo apps**, **frontends** and **backends** which showcase examples and tutorials
* **org apps**, **frontends** and **backends** which implement real business functionnality


.. image:: ../diagrams/pigal_development_cycle.drawio.svg


The development cycle uses three project types:

* **template projects** offer a reusable foundation and pre-configured structure to start new projects
* **module projects** are customized from templates projects to address specific business domains
* **application projects** integrate multiple modules projects to form a complete web application



Project collaboration
---------------------


So application projects are built by assembling multiple module projects created from template projects:

* **full-stack developers** can create and share template project
* **frontend developpers** will create frontends in module projects
* **backend developpers** will create backends in module projects
* **project managers** can finally assemble these module into application projects

.. TIP::
    frontend developpers can also develop theme for projects.


Share project directory
-----------------------

All these projects are directory that can be shared (as zip file or git repo for example). 
Any developper will simple paste or unzip file into a project directory.

.. IMPORTANT::
    before project app execution, a **virtual env** must always be created. 
    Developpers must then always provide a ``requirements.txt`` when sharing their project.
    

Share module directory
----------------------

Even modules (backend or frontend) are directory that can be shared. 

By simply **copying and pasting module directory** inside appropriate project sub-directory:

* ``frontend`` directory must be copied inside ``frontends`` directory
* ``backend`` directory must be copied inside ``backends`` directory

The copied module will be automatically registered inside Flask app.


.. IMPORTANT::
    A module can be shared without errors between project using same extensions.
