Installation
============

Requirements
------------

- Python 3.8 or higher
- ``pycountry``
- ``pycountry-convert``

Install from PyPI
-----------------

.. code-block:: bash

    pip install smartbindb

Install from source
-------------------

.. code-block:: bash

    git clone https://github.com/abirxdhack/TheSmartBinDB
    cd TheSmartBinDB
    pip install -e .

Verify installation
-------------------

.. code-block:: python

    import smartbindb
    print(smartbindb.__version__)

Optional development extras
---------------------------

.. code-block:: bash

    pip install "smartbindb[dev]"
    pip install "smartbindb[docs]"
