
Customizing Home pages
======================

You can change home pages and navigation created by default.
So how would you then actually implement that?


Default Home
------------

To illustrate this, we suppose that 
we have created a project called ``demo``.
This project will contain ``/pages/home`` directory 
with the following structure:

.. code-block::

    /home            
    |-- /static           # static files
    |-- /templates        # jinja templates
    |   |-- /home         # home pages templates
    |   |-- /examples     # examples pages templates
    |
    |-- __init__.py       # home initialization
    |-- forms.py          # home WTF-forms
    |-- routes.py         # home routing
    |   

