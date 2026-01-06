
Sharing projects
================

Application projects are built by assembling modules projects created from template projects. So:

* **Template developers** create and share template projects to help other developers
* **Module developers** create and share module projects to meet real business needs
* **Application developers** collect and integrate module projects

Module developers can also need to share parts of their projects:

* frontends can be shared between frontend developers working on different projects
* backends can also be shared between backend developers working on different projects

So how can we share:

* template projects (see :ref:`Share template project`)
* module projects (see :ref:`Share module project`)
* frontend only (see :ref:`Share frontend`)
* backend only (see :ref:`Share backend`)


Share template project
----------------------

Template project are directory that can be shared in two steps:

* Template developer create the project **zip file or git repo**
* Module developer clone or download the project **zip file or git repo**

.. IMPORTANT::
    It is required that:

    * template developers share template projects with updated ``requirements.txt``
    * module developers create **virtual env** with template projets ``requirements.txt``, before using them
    

Share module project
--------------------

Module project are also directory that can be shared in two steps:

* Module developer create the project **zip file or git repo**
* Application developer clone or download the project **zip file or git repo**

Integrating modules project into application project 
is a critical and complex task (see :ref:`Projects integration`). 

.. IMPORTANT::
    It is required that module developers share module projects with updated ``requirements.txt``



Share frontend
--------------

Frontend are directory that can be shared in two steps:

* copy the frontend from the ``frontends`` directory of a **source project** 
* paste the frontend into the ``frontends`` directory of a **destination project**

The copied frontend will be automatically registered inside Flask app.

.. IMPORTANT::
    a frontend can be shared without errors if source project and destination project have the **same UI System**. 
    The UI System is indicated in theme filename (the theme ``MyTheme_xy.zip`` use ``xy`` ui system for example). So:

    * a project using ``MyTheme_xy`` has the same ui system with a project using ``OtherTheme_xy``
    * a project using ``MyTheme_xy`` has not the same ui system with a project using ``MyTheme_abc``



Share backend
--------------

As frontend, backend can be shared in two steps:

* copy the backend from the ``backends`` directory of a **source project** 
* paste the backend into the ``backends`` directory of a **destination project**

The copied backend will be automatically registered inside Flask app.

Pigal-Flask provides advanced functionnalities for other usual problems 
(see :ref:`Advanced functionnalities`).

