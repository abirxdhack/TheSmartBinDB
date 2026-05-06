Changelog
=========

5.17.2
------

- Refreshed documentation site with the SmartBinDB design system, custom
  Furo theme overrides, and an expanded tutorial / examples / advanced
  section tree.
- Added FastAPI, Flask, Django and Telegram bot integration tutorials.
- Documented the response envelope, data model, and internals.

5.17.1
------

- Initial public packaging on PyPI as ``smartbindb``.
- Bundled offline binary BIN database (``smartbin.db``).
- Async lookup methods: ``get_bin_info``, ``get_bins_by_bank``,
  ``get_bins_by_country``.
- ISO country metadata via ``pycountry`` and ``pycountry-convert``.
