FAQ
===

Is SmartBinDB free to use?
--------------------------

Yes. The library is MIT licensed and the bundled dataset has no
per-lookup cost.

Does SmartBinDB make network calls?
-----------------------------------

No. Every lookup is served from the in-process database. SmartBinDB does
not import an HTTP client, send telemetry, or read configuration files.

How fresh is the bundled data?
------------------------------

The dataset snapshot is rebuilt at release time. Watch the GitHub
repository for new tagged releases.

How big is the install?
-----------------------

The wheel is roughly 50 MB on disk because of the bundled binary database.
At runtime the deserialized data is approximately 150–250 MB of RAM
depending on Python version and platform.

How do I keep memory low in serverless / lambda environments?
-------------------------------------------------------------

Construct ``SmartBinDB`` exactly once per process and reuse it across
invocations. If you only need country metadata and not BIN coverage, do
not import SmartBinDB at all — use ``pycountry`` directly.

Can I add my own BINs?
----------------------

The bundled binary file is a pickle. The supported workflow is to open a
PR against the upstream dataset on GitHub. Manual mutation of
``BIN_INDEX`` / ``COUNTRY_DATA`` at runtime is technically possible but not
supported across releases.

Does it support Luhn validation of PANs?
----------------------------------------

The library exposes a ``Luhn`` flag on every successful response to mark
BIN ranges that participate in Luhn-conformant numbering schemes. A
reference Luhn implementation is shown in :doc:`luhn-validation`.

What Python versions are supported?
-----------------------------------

Python 3.8 through 3.12.
