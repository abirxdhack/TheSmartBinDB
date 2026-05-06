CLI tool
========

A small ``argparse`` based CLI that prints BIN, bank or country lookups.

.. code-block:: python

    import argparse
    import asyncio
    import json
    from smartbindb import SmartBinDB

    db = SmartBinDB()

    async def run(args):
        if args.bin:
            return await db.get_bin_info(args.bin)
        if args.bank:
            return await db.get_bins_by_bank(args.bank, limit=args.limit)
        if args.country:
            return await db.get_bins_by_country(args.country, limit=args.limit)
        return {"status": "error", "message": "no query given"}

    def main():
        parser = argparse.ArgumentParser(prog="smartbindb")
        parser.add_argument("--bin")
        parser.add_argument("--bank")
        parser.add_argument("--country")
        parser.add_argument("--limit", type=int, default=10)
        args = parser.parse_args()
        result = asyncio.run(run(args))
        print(json.dumps(result, indent=2, default=str))

    if __name__ == "__main__":
        main()

Save as ``cli.py`` and run::

    python cli.py --bin 457173
    python cli.py --bank "Chase" --limit 5
    python cli.py --country BD --limit 20
