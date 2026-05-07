Enriching a CSV of BINs
=======================

Read a CSV with a ``bin`` column, enrich each row with issuer and country,
and write the output to a new CSV.

.. code-block:: python

    import asyncio
    import csv
    from smartbindb import SmartBinDB

    db = SmartBinDB()

    async def enrich(rows):
        results = await asyncio.gather(*(db.get_bin_info(r["bin"]) for r in rows))
        for row, result in zip(rows, results):
            if result["status"] == "SUCCESS":
                d = result["data"][0]
                row["brand"] = d["brand"]
                row["issuer"] = d["issuer"]
                row["country"] = d["Country"]["Name"]
                row["type"] = d["type"]
            else:
                row["brand"] = row["issuer"] = row["country"] = row["type"] = ""
        return rows

    def main():
        with open("input.csv", newline="") as f:
            rows = list(csv.DictReader(f))
        rows = asyncio.run(enrich(rows))
        fieldnames = list(rows[0].keys())
        with open("output.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    if __name__ == "__main__":
        main()
