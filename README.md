# SmartBinDB

[![PyPI version](https://img.shields.io/pypi/v/smartbindb.svg)](https://pypi.org/project/smartbindb/)
[![Python versions](https://img.shields.io/pypi/pyversions/smartbindb.svg)](https://pypi.org/project/smartbindb/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-online-blue)](https://abirxdhack.github.io/TheSmartBinDB)

> Blazing-fast **offline** Bank Identification Number (BIN) lookup database for Python.

SmartBinDB ships with a bundled binary database covering hundreds of thousands of
card BINs across the globe and provides a simple async API to look them up by
BIN, issuing bank or country — with **zero network calls**.

## Installation

```bash
pip install smartbindb
```

## Quick start

```python
import asyncio
from smartbindb import SmartBinDB

db = SmartBinDB()

async def main():
    print(await db.get_bin_info("457173"))
    print(await db.get_bins_by_bank("Chase", limit=5))
    print(await db.get_bins_by_country("BD", limit=10))

asyncio.run(main())
```

## Documentation

Full API documentation, tutorials, integration guides (FastAPI, Flask, Django,
Telegram bots) and examples live at:
<https://abirxdhack.github.io/TheSmartBinDB>

## Links

- Repository: <https://github.com/abirxdhack/TheSmartBinDB>
- PyPI: <https://pypi.org/project/smartbindb/>
- Issues: <https://github.com/abirxdhack/TheSmartBinDB/issues>

## License

MIT © Abir Arafat Chawdhury
