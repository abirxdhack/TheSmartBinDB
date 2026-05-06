Integrating SmartBinDB with Flask
=================================

Flask is synchronous by default. You can use SmartBinDB by running the
async coroutine via ``asyncio.run`` or by switching to Flask's async views.

Sync wrapper
------------

.. code-block:: python

    import asyncio
    from flask import Flask, jsonify, abort
    from smartbindb import SmartBinDB

    app = Flask(__name__)
    db = SmartBinDB()

    def run(coro):
        return asyncio.run(coro)

    @app.get("/bin/<bin_value>")
    def lookup(bin_value):
        result = run(db.get_bin_info(bin_value))
        if result["status"] != "SUCCESS":
            abort(404, result["message"])
        return jsonify(result["data"][0])

    @app.get("/bank/<name>")
    def bank(name):
        return jsonify(run(db.get_bins_by_bank(name, limit=25)))

Async views (Flask 2+)
----------------------

.. code-block:: python

    from flask import Flask, jsonify
    from smartbindb import SmartBinDB

    app = Flask(__name__)
    db = SmartBinDB()

    @app.get("/bin/<bin_value>")
    async def lookup(bin_value):
        return jsonify(await db.get_bin_info(bin_value))
