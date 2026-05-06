Looking up BINs by issuing bank
===============================

Use :meth:`SmartBinDB.get_bins_by_bank` to discover every BIN whose issuer
name matches a case-insensitive substring.

Basic usage
-----------

.. code-block:: python

    import asyncio
    from smartbindb import SmartBinDB

    db = SmartBinDB()

    async def main():
        result = await db.get_bins_by_bank("Chase", limit=10)
        for entry in result["data"]:
            print(entry["bin"], "-", entry["issuer"], "-", entry["country_code"])

    asyncio.run(main())

How matching works
------------------

The needle is lowercased and substring-matched against the ``issuer`` field
of every BIN entry. ``"chase"``, ``"Chase"`` and ``"CHASE BANK"`` all match
records whose issuer contains the case-folded fragment ``"chase"``.

Capping result size
-------------------

Pass ``limit`` to bound the number of returned records. SmartBinDB stops
scanning the in-memory database as soon as the limit is satisfied, so this
also reduces CPU work.

.. code-block:: python

    await db.get_bins_by_bank("Standard Chartered", limit=50)

Pagination pattern
------------------

The library does not maintain server-side cursors. To paginate, fetch a
larger window and slice client-side:

.. code-block:: python

    import asyncio
    from smartbindb import SmartBinDB

    db = SmartBinDB()
    PAGE = 25

    async def page(bank: str, n: int):
        full = await db.get_bins_by_bank(bank, limit=PAGE * (n + 1))
        if full["status"] != "SUCCESS":
            return []
        return full["data"][n * PAGE : (n + 1) * PAGE]

    print(asyncio.run(page("HSBC", 0)))
    print(asyncio.run(page("HSBC", 1)))

Aggregating across banks
------------------------

.. code-block:: python

    import asyncio
    from collections import Counter
    from smartbindb import SmartBinDB

    db = SmartBinDB()

    async def by_country(bank: str):
        result = await db.get_bins_by_bank(bank, limit=10_000)
        if result["status"] != "SUCCESS":
            return Counter()
        return Counter(e["country_code"] for e in result["data"])

    print(asyncio.run(by_country("Citi")).most_common(10))
