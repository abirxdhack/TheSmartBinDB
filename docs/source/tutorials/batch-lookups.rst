Batch lookups
=============

SmartBinDB does not need a dedicated batch endpoint — because every lookup
is an in-memory ``dict`` hit, you can simply ``asyncio.gather`` as many
lookups as you need.

Concurrent BIN lookups
----------------------

.. code-block:: python

    import asyncio
    from smartbindb import SmartBinDB

    db = SmartBinDB()

    async def lookup_many(bins):
        return await asyncio.gather(*(db.get_bin_info(b) for b in bins))

    results = asyncio.run(lookup_many(["457173", "414709", "555555", "424242"]))
    for r in results:
        if r["status"] == "SUCCESS":
            print(r["data"][0]["bin"], r["data"][0]["issuer"])

Bulk enrichment of a list of PANs
---------------------------------

.. code-block:: python

    import asyncio
    from smartbindb import SmartBinDB

    db = SmartBinDB()

    PANS = [
        "4571730000000000",
        "5555555555554444",
        "378282246310005",
    ]

    async def enrich(pans):
        results = await asyncio.gather(*(db.get_bin_info(p[:8]) for p in pans))
        for pan, result in zip(pans, results):
            if result["status"] == "SUCCESS":
                row = result["data"][0]
                print(pan, "->", row["brand"], row["Country"]["Name"])
            else:
                print(pan, "-> not found")

    asyncio.run(enrich(PANS))

Dedupe before lookup
--------------------

If you are processing large CSVs, dedupe the BIN prefixes before scheduling
lookups to reduce work:

.. code-block:: python

    import asyncio
    from smartbindb import SmartBinDB

    db = SmartBinDB()

    async def enrich_unique(pans):
        bins = sorted({p[:8] for p in pans})
        results = await asyncio.gather(*(db.get_bin_info(b) for b in bins))
        index = {b: r for b, r in zip(bins, results)}
        return [index[p[:8]] for p in pans]
