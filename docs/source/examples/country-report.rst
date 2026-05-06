Country coverage report
=======================

Build a markdown table summarizing how many BINs are bundled per country.

.. code-block:: python

    from smartbindb import SmartBinDB

    db = SmartBinDB()
    print("| Code | Country | Continent | BINs |")
    print("|------|---------|-----------|------|")
    rows = []
    for code, entries in db.COUNTRY_DATA.items():
        info = db.get_country_info(code)
        rows.append((code, info["Name"], info["Cont"], len(entries)))

    rows.sort(key=lambda r: -r[3])
    for code, name, cont, n in rows:
        print(f"| {code} | {name} | {cont} | {n} |")
