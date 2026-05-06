Quickstart
==========

Install SmartBinDB from PyPI::

    pip install smartbindb

Look up a single BIN
--------------------

.. code-block:: python

    import asyncio
    from smartbindb import SmartBinDB

    db = SmartBinDB()

    async def main():
        result = await db.get_bin_info("457173")
        print(result)

    asyncio.run(main())

Search BINs by issuing bank
---------------------------

.. code-block:: python

    import asyncio
    from smartbindb import SmartBinDB

    db = SmartBinDB()

    async def main():
        result = await db.get_bins_by_bank("Chase", limit=10)
        for entry in result["data"]:
            print(entry["bin"], entry["issuer"], entry["country_code"])

    asyncio.run(main())

List BINs by country
--------------------

.. code-block:: python

    import asyncio
    from smartbindb import SmartBinDB

    db = SmartBinDB()

    async def main():
        result = await db.get_bins_by_country("BD", limit=20)
        print("Total:", result["count"])
        for entry in result["data"][:5]:
            print(entry["bin"], entry["issuer"])

    asyncio.run(main())

Inspect ISO country metadata
----------------------------

.. code-block:: python

    from smartbindb import SmartBinDB

    db = SmartBinDB()
    print(db.get_country_info("US"))
    print(db.get_country_info("DE"))
    print(db.get_country_info("BD"))
