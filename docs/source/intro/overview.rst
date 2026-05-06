Overview
========

SmartBinDB is a fully offline Python library for looking up Bank Identification
Numbers (BINs) — the first 6–8 digits of a payment card that identify the
issuing institution, brand, and country. Every lookup is served from a
bundled binary database that is loaded into memory once at startup, so all
queries are O(1) hash lookups with no network round-trips.

Key features
------------

- **Offline first.** The full BIN dataset ships inside the wheel. No API keys,
  no rate limits, no network dependency, and no PII ever leaves the host.
- **Async API.** All lookup methods are coroutines, so SmartBinDB drops
  cleanly into FastAPI, aiohttp, Telegram bots, asyncio workers, and any
  other event-loop based application.
- **Hundreds of thousands of BINs.** The bundled database covers card BINs
  from 200+ country buckets, including separate ``US``, ``US1`` and ``US2``
  regional aggregates that are merged automatically when you query ``US``.
- **Rich response payload.** Every hit includes the BIN, brand, category,
  card tier, type (debit/credit/prepaid), issuer, phone, website, and full
  ISO country metadata (alpha-2, alpha-3, numeric code, English name,
  continent).
- **Typed.** SmartBinDB ships ``py.typed`` and exposes a small, well-typed
  public surface area suitable for static analysis.

When to use SmartBinDB
----------------------

- You need to enrich card BINs at scale without paying per-lookup API fees.
- You need predictable, sub-millisecond lookups inside an async hot path.
- You operate in a network-restricted environment (air-gapped clusters,
  PCI-segmented networks, on-prem fraud pipelines).
- You want a single dependency that bundles its data instead of pulling
  files at runtime.

When *not* to use SmartBinDB
----------------------------

- You require real-time bank/issuer mutations (mergers, rebrands within the
  last 24 hours). The bundled snapshot is updated at release time.
- You need card *number* validation beyond Luhn — SmartBinDB is a BIN
  database, not a payment processor.
