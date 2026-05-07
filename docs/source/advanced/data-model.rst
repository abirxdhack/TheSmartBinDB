Data model
==========

SmartBinDB stores its bundled dataset in a single binary pickle file at
``smartbindb/data/smartbin.db``. The file deserializes to a dict with two
top-level entries:

.. code-block:: text

    {
      "country_data": { "BD": [<entry>, <entry>, ...], "US1": [...], ... },
      "bin_index":    { "457173": ("BD", <entry>), ... }
    }

Country buckets
---------------

The ``country_data`` map is keyed by alpha-2 country code. The United States
is split across three buckets — ``US``, ``US1`` and ``US2`` — to keep the
internal lists at a manageable size. The public method
:meth:`SmartBinDB.get_bins_by_country` transparently merges those buckets
when you query ``"US"`` and caps the response at 8000 records.

BIN index
---------

The ``bin_index`` map is keyed by the BIN string itself and maps to a
``(country_code, entry)`` tuple. This is what powers the O(1) lookup in
:meth:`SmartBinDB.get_bin_info`.

Entry shape
-----------

Each raw entry contains the following keys (any of which may be absent or
empty for legacy rows):

- ``bin`` — the BIN string.
- ``brand`` — card brand.
- ``category`` — product category.
- ``type`` — card type.
- ``country_code_alpha3`` — alpha-3 country code.
- ``issuer`` — issuing bank.
- ``phone`` — customer service phone.
- ``website`` — issuer website.

The :meth:`SmartBinDB.format_entry` method normalizes raw entries into the
public schema documented in :doc:`response-schema`.
