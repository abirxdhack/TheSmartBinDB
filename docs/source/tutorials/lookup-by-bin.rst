Looking up a single BIN
=======================

The most common SmartBinDB workflow is enriching a single card BIN —
typically the first 6 to 8 digits of a payment card number — with issuer,
country and brand metadata.

Basic usage
-----------

.. code-block:: python

    import asyncio
    from smartbindb import SmartBinDB

    db = SmartBinDB()

    async def lookup(bin_value: str):
        result = await db.get_bin_info(bin_value)
        if result["status"] != "SUCCESS":
            print("Not found:", result["message"])
            return
        record = result["data"][0]
        print("BIN:        ", record["bin"])
        print("Brand:      ", record["brand"])
        print("Type:       ", record["type"])
        print("Category:   ", record["category"])
        print("Card tier:  ", record["CardTier"])
        print("Issuer:     ", record["issuer"])
        print("Country:    ", record["Country"]["Name"])
        print("Continent:  ", record["Country"]["Cont"])
        print("Phone:      ", record["phone"])
        print("Website:    ", record["website"])

    asyncio.run(lookup("457173"))

Accepted input
--------------

- A string of digits, typically 6 to 8 characters wide.
- Leading or trailing whitespace is stripped automatically.
- Non-string input is coerced via ``str()``.

If the BIN is not present in the bundled database the response is::

    {"status": "error",
     "message": "No matches found for BIN: 999999",
     "api_owner": "@ISmartCoder",
     "api_channel": "@TheSmartDev"}

Truncating long PANs
--------------------

If you only have full PANs, slice them down to the BIN before calling:

.. code-block:: python

    import asyncio
    from smartbindb import SmartBinDB

    db = SmartBinDB()

    async def from_pan(pan: str):
        bin_value = pan.replace(" ", "")[:8]
        return await db.get_bin_info(bin_value)

    print(asyncio.run(from_pan("4571 7300 0000 0000")))

Verifying availability before lookup
------------------------------------

If you want to check that the underlying database is loaded before issuing
queries (for example inside a health check endpoint), inspect ``BIN_INDEX``
directly:

.. code-block:: python

    db = SmartBinDB()
    assert db.BIN_INDEX, "smartbin.db failed to load"
