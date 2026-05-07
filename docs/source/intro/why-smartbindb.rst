Why SmartBinDB?
===============

There are several BIN lookup services in the wild. SmartBinDB is opinionated
about a small set of trade-offs.

Offline by design
-----------------

Most BIN APIs charge per request, throttle aggressively, or require an API
key with PII exposure. SmartBinDB ships the entire dataset inside the wheel
and performs every lookup in-process. There is no HTTP client, no
authentication, and no telemetry.

Predictable latency
-------------------

Every lookup is backed by an in-memory ``dict`` index built at startup. The
first call to :meth:`SmartBinDB.get_bin_info` after construction is the only
"slow" call — it deserializes the bundled database once. After that, lookups
are constant-time hash hits, typically in the microseconds.

Async-first
-----------

The public API is async so that SmartBinDB composes naturally with FastAPI,
aiohttp, Discord/Telegram bots, and any worker that already has an event
loop. There is no thread-pool indirection — the underlying lookups are
synchronous in-memory operations wrapped as coroutines for ergonomic use
inside ``await`` chains.

Uniform response schema
-----------------------

Every public lookup returns the same envelope:

.. code-block:: text

    {
      "status": "SUCCESS" | "error",
      "data":   [...],         # only on SUCCESS
      "count":  <int>,         # only on SUCCESS
      "filtered_by": "bin" | "bank" | "country",
      "api_owner":   "@ISmartCoder",
      "api_channel": "@TheSmartDev",
      "Luhn": True
    }

This means you can write generic enrichment code that does not branch on the
caller-facing method.

Comparison with hosted APIs
---------------------------

+--------------------+---------------------+------------------------+
| Feature            | Hosted BIN API      | SmartBinDB             |
+====================+=====================+========================+
| Network calls      | Yes (per lookup)    | No                     |
+--------------------+---------------------+------------------------+
| Rate limits        | Yes                 | No                     |
+--------------------+---------------------+------------------------+
| Cost per lookup    | $$                  | Free                   |
+--------------------+---------------------+------------------------+
| Data residency     | Vendor controlled   | Local process          |
+--------------------+---------------------+------------------------+
| Offline support    | No                  | Yes                    |
+--------------------+---------------------+------------------------+
| Async API          | Varies              | Yes                    |
+--------------------+---------------------+------------------------+
