Error handling
==============

SmartBinDB never raises for "lookup miss" conditions — instead, it returns a
structured error envelope. Real exceptions are reserved for programmer
errors (e.g. passing wrong types) or environmental failures (database file
missing).

Error envelope
--------------

.. code-block:: python

    {
      "status":      "error",
      "message":     "No matches found for BIN: 999999",
      "api_owner":   "@ISmartCoder",
      "api_channel": "@TheSmartDev"
    }

Common patterns
---------------

.. code-block:: python

    import asyncio
    from smartbindb import SmartBinDB

    db = SmartBinDB()

    async def safe_lookup(bin_value: str):
        result = await db.get_bin_info(bin_value)
        if result["status"] != "SUCCESS":
            return None
        return result["data"][0]

    print(asyncio.run(safe_lookup("000000")))

Centralizing error handling
---------------------------

.. code-block:: python

    import asyncio
    from smartbindb import SmartBinDB

    db = SmartBinDB()

    class BinLookupError(Exception):
        pass

    async def lookup_or_raise(bin_value: str):
        result = await db.get_bin_info(bin_value)
        if result["status"] != "SUCCESS":
            raise BinLookupError(result["message"])
        return result["data"][0]

    try:
        print(asyncio.run(lookup_or_raise("000000")))
    except BinLookupError as exc:
        print("Lookup failed:", exc)

Failure modes worth handling
----------------------------

- **Database missing.** If ``smartbin.db`` is removed from the package the
  first lookup returns an error indicating the path. Ship the binary file
  alongside your application or pin to a wheel built with it included.
- **Unknown country code.** :meth:`SmartBinDB.get_bins_by_country` returns
  an error envelope rather than raising.
- **Empty result set.** Bank substring searches with no matches return an
  error envelope with the original query echoed back.
