Issuer analytics
================

Compute the top issuers by number of BINs across the whole database.

.. code-block:: python

    from collections import Counter
    from smartbindb import SmartBinDB

    db = SmartBinDB()
    counter = Counter()

    for entries in db.COUNTRY_DATA.values():
        for entry in entries:
            issuer = (entry.get("issuer") or "").strip()
            if issuer:
                counter[issuer] += 1

    for issuer, count in counter.most_common(25):
        print(f"{count:6d}  {issuer}")

Top brands
----------

.. code-block:: python

    from collections import Counter
    from smartbindb import SmartBinDB

    db = SmartBinDB()
    brands = Counter()
    for entries in db.COUNTRY_DATA.values():
        for entry in entries:
            brand = (entry.get("brand") or "").upper()
            if brand:
                brands[brand] += 1

    for brand, count in brands.most_common():
        print(brand, count)
