Response schema
===============

Every successful SmartBinDB response shares the same envelope:

.. code-block:: text

    {
      "status":      "SUCCESS",
      "data":        [ <BinRecord>, ... ],
      "count":       <int>,
      "filtered_by": "bin" | "bank" | "country",
      "api_owner":   "@ISmartCoder",
      "api_channel": "@TheSmartDev",
      "Luhn":        true
    }

Every failed response shares this envelope:

.. code-block:: text

    {
      "status":      "error",
      "message":     <str>,
      "api_owner":   "@ISmartCoder",
      "api_channel": "@TheSmartDev"
    }

BinRecord
---------

.. code-block:: text

    {
      "bin":                  "457173",
      "brand":                "VISA",
      "category":             "CLASSIC",
      "CardTier":             "CLASSIC VISA",
      "country_code":         "BD",
      "country_code_alpha3":  "BGD",
      "Type":                 "credit",
      "type":                 "credit",
      "Country": {
        "A2":   "BD",
        "A3":   "BGD",
        "N3":   "050",
        "Name": "Bangladesh",
        "Cont": "Asia"
      },
      "issuer":  "Brac Bank Limited",
      "phone":   "+88 09678 016 230",
      "website": "https://www.bracbank.com/"
    }

Field reference
---------------

- ``bin`` — the matching BIN string from the database.
- ``brand`` — card brand (e.g. ``VISA``, ``MASTERCARD``, ``AMEX``).
- ``category`` — sub-product category (e.g. ``CLASSIC``, ``GOLD``, ``PLATINUM``).
- ``CardTier`` — concatenation of ``category`` and ``brand`` for display.
- ``country_code`` — alpha-2 country bucket the BIN was indexed under.
- ``country_code_alpha3`` — alpha-3 ISO code from the database, when present.
- ``Type`` / ``type`` — card type (``debit``, ``credit``, ``prepaid``).
- ``Country`` — see :func:`smartbindb.SmartBinDB.get_country_info`.
- ``issuer`` — issuing bank name as recorded in the dataset.
- ``phone`` — issuer customer service phone, when known.
- ``website`` — issuer website, when known.
