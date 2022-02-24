Installation Guide
***********************************

Supported Python versions
=========================
Diplomatic pulse requires Python 3.6+.



Installing Diplomatic pulse
===========================
To start Diplomatic pulse using Docker containers, run:

::

   git clone git@github.com:qcri/DiplomaticPulse.git
   docker-compose up

Alternatively, if you can run a specific spider locally :

::

   pip install scrapy
   pip install -r requirements.txt
   scrapy crawl <spider-name> -a url=<page url>

We strongly recommend that you install Scrapy in `a dedicated virtualenv`_, to avoid conflicting with your system packages.


.. _a dedicated virtualenv:
.. _virtualenv: https://docs.python.org/3/tutorial/venv.html#tut-venv

Using a virtual environment (recommended)
=========================================
We recommend installing Diplomatic pulse inside a virtual environment on all platforms.

Instead, we recommend that you install Diplomatic pulse within a so-called "virtual environment" (**venv**). Virtual environments allow
you to not conflict with already-installed Python system packages (which could break some of your system tools and scripts), and
still install packages normally with ``pip`` (without ``sudo`` and the likes).

See `Virtual Environments and Packages`_ on how to create your virtual environment.

.. _Platform specific installation notes:

Platform specific installation notes
====================================
Ubuntu 14.04 or above
---------------------
Diplomatic pulse is currently with Ubuntu 14.04.

To install Scrapy on Ubuntu (or Ubuntu-based) systems, you need to install these dependencies:

``sudo apt-get install python3 python3-dev python3-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev``

* ``python3-dev, zlib1g-dev, libxml2-dev`` and ``libxslt1-dev`` are required for ``lxml``
* ``libssl-dev`` and ``libffi-dev`` are required for ``cryptography``

Inside a `virtualenv`_, you can install Scrapy with ``pip`` after that:

``pip install scrapy``
