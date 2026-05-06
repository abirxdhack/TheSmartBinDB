"""SmartBinDB — blazing-fast offline BIN lookup library with sync/async support.

Bundled database of hundreds of thousands of card BINs across country buckets.
Lookups served from in-memory dict index built once at startup — all queries
are O(1) hash hits, never touch the network.

Public API consists of single :class:`SmartBinDB` class with six lookup methods:

Synchronous:

* :meth:`SmartBinDB.get_bin_info` — exact BIN match.
* :meth:`SmartBinDB.get_bins_by_bank` — issuer substring match.
* :meth:`SmartBinDB.get_bins_by_country` — country code lookup.

Asynchronous:

* :meth:`SmartBinDB.aget_bin_info` — async exact BIN match.
* :meth:`SmartBinDB.aget_bins_by_bank` — async issuer match.
* :meth:`SmartBinDB.aget_bins_by_country` — async country lookup.

Example — Sync
--------------

.. code-block:: python

    from smartbindb import SmartBinDB

    db = SmartBinDB()
    result = db.get_bin_info("457173")
    print(result)

Example — Async
---------------

.. code-block:: python

    import asyncio
    from smartbindb import SmartBinDB

    db = SmartBinDB()

    async def main():
        result = await db.aget_bin_info("457173")
        print(result)

    asyncio.run(main())

Documentation site: https://abirxdhack.github.io/TheSmartBinDB
"""

from .smartdb import SmartBinDB

__version__ = "5.17.4"
__author__ = "Abir Arafat Chawdhury"
__license__ = "MIT"
__all__ = ["SmartBinDB", "__version__"]
