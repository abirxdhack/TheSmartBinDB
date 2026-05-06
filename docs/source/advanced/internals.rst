Internals
=========

This page documents the moving parts inside SmartBinDB so contributors can
reason about behaviour and performance.

Startup
-------

1. ``SmartBinDB.__init__`` records ``START_TIME`` and computes
   ``BINARY_DB`` (the path to ``smartbin.db``).
2. ``load_data`` is called immediately. It opens the pickle file and
   populates ``COUNTRY_DATA`` and ``BIN_INDEX`` in-process.
3. If the file is missing or unreadable, the error is logged and the
   indices remain empty. The next public call will retry the load before
   returning an error envelope.

Lookup paths
------------

- :meth:`SmartBinDB.get_bin_info` is a single ``BIN_INDEX[key]`` access.
- :meth:`SmartBinDB.get_bins_by_country` reads a single bucket out of
  ``COUNTRY_DATA``, except for the ``US`` pseudo-code which iterates
  ``US``, ``US1`` and ``US2`` in order.
- :meth:`SmartBinDB.get_bins_by_bank` performs a linear scan across every
  country bucket and matches the lower-cased substring of the issuer.

Caching
-------

:func:`functools.lru_cache` is applied to :meth:`SmartBinDB.get_country_info`
with a maxsize of 256, which is enough to cover every alpha-2 in the
database. ``pycountry`` lookups are non-trivial, so caching makes a
measurable difference in tight enrichment loops.

Logging
-------

SmartBinDB logs through the standard ``logging`` module under the
``smartbindb`` logger name. Increase verbosity with::

    import logging
    logging.getLogger("smartbindb").setLevel(logging.DEBUG)
