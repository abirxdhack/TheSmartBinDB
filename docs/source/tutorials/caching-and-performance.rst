Caching and performance
=======================

SmartBinDB is already an in-memory database — the hot path is a single
``dict`` lookup. The advice in this page is about *amortizing* the
one-time setup cost and avoiding re-doing work.

One database per process
------------------------

Construct ``SmartBinDB`` exactly once per process and reuse it across
requests. The constructor deserializes a 50+ MB pickle and builds the BIN
index, so you do *not* want to do it per request.

.. code-block:: python

    from smartbindb import SmartBinDB

    DB = SmartBinDB()

    async def handle(req):
        return await DB.get_bin_info(req.bin)

Lazy import for slow startup paths
----------------------------------

If your CLI must boot quickly, defer the construction:

.. code-block:: python

    from functools import lru_cache

    @lru_cache(maxsize=1)
    def get_db():
        from smartbindb import SmartBinDB
        return SmartBinDB()

Caching the public envelope
---------------------------

If the same BIN is queried very frequently you can cache the entire
response envelope using :func:`functools.lru_cache` on a sync wrapper or
``aiocache`` on the coroutine:

.. code-block:: python

    import asyncio
    from functools import lru_cache
    from smartbindb import SmartBinDB

    db = SmartBinDB()

    @lru_cache(maxsize=4096)
    def lookup_sync(bin_value: str):
        return asyncio.get_event_loop().run_until_complete(db.get_bin_info(bin_value))

For async caches, use ``aiocache`` or ``async-lru``:

.. code-block:: python

    from async_lru import alru_cache

    @alru_cache(maxsize=4096)
    async def cached_lookup(bin_value: str):
        return await db.aget_bin_info(bin_value)

Memory footprint
----------------

The deserialized dataset uses roughly 150–250 MB of RAM depending on Python
version and platform. If you are running on memory-constrained hosts,
prefer one shared SmartBinDB instance per worker rather than per
sub-interpreter.
