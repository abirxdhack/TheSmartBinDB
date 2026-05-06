Bulk PAN validator
==================

Validate a list of PANs (Luhn) and enrich the BIN portion in one pass.

.. code-block:: python

    import asyncio
    from smartbindb import SmartBinDB

    db = SmartBinDB()

    def luhn_ok(pan: str) -> bool:
        digits = [int(c) for c in pan if c.isdigit()]
        checksum = 0
        for i, d in enumerate(reversed(digits)):
            if i % 2 == 1:
                d *= 2
                if d > 9:
                    d -= 9
            checksum += d
        return checksum % 10 == 0

    async def validate(pans):
        results = await asyncio.gather(*(db.get_bin_info(p[:8]) for p in pans))
        report = []
        for pan, result in zip(pans, results):
            ok = luhn_ok(pan)
            row = {"pan": pan, "luhn": ok}
            if result["status"] == "SUCCESS":
                d = result["data"][0]
                row.update(brand=d["brand"], issuer=d["issuer"], country=d["Country"]["Name"])
            else:
                row.update(brand="?", issuer="?", country="?")
            report.append(row)
        return report

    if __name__ == "__main__":
        pans = ["4571730000000000", "5555555555554444", "378282246310005"]
        for r in asyncio.run(validate(pans)):
            print(r)
