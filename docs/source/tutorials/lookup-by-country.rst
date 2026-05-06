Looking up BINs by country
==========================

Use :meth:`SmartBinDB.get_bins_by_country` to enumerate every BIN issued in
a given country bucket.

Basic usage
-----------

.. code-block:: python

    import asyncio
    from smartbindb import SmartBinDB

    db = SmartBinDB()

    async def main():
        result = await db.get_bins_by_country("BD", limit=20)
        print("count:", result["count"])
        for entry in result["data"][:5]:
            print(entry["bin"], entry["issuer"])

    asyncio.run(main())

Country code semantics
----------------------

- The argument is upper-cased internally, so ``"bd"`` and ``"BD"`` are
  equivalent.
- The pseudo code ``"US"`` aggregates the ``US``, ``US1`` and ``US2``
  regional buckets and is capped at ``8000`` records per call.
- Any code that is not present in the bundled dataset returns an error
  response — call :meth:`SmartBinDB.get_country_info` first if you only need
  ISO metadata for an unsupported code.

Capped retrieval
----------------

.. code-block:: python

    await db.get_bins_by_country("DE", limit=100)
    await db.get_bins_by_country("US", limit=5000)

Stream every BIN of a country
-----------------------------

.. code-block:: python

    import asyncio
    from smartbindb import SmartBinDB

    db = SmartBinDB()

    async def dump(country: str):
        result = await db.get_bins_by_country(country, limit=None)
        if result["status"] != "SUCCESS":
            return
        for entry in result["data"]:
            yield entry

    async def main():
        async for entry in dump("BD"):
            print(entry["bin"], entry["issuer"])

    asyncio.run(main())

Country coverage discovery
--------------------------

To enumerate the country buckets actually present in the bundled database,
inspect :attr:`SmartBinDB.COUNTRY_DATA` directly:

.. code-block:: python

    from smartbindb import SmartBinDB

    db = SmartBinDB()
    for code in sorted(db.COUNTRY_DATA):
        info = db.get_country_info(code)
        print(code, info["Name"], len(db.COUNTRY_DATA[code]))
