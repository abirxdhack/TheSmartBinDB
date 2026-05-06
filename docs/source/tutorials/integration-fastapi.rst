Integrating SmartBinDB with FastAPI
===================================

SmartBinDB plugs straight into FastAPI: instantiate the database once at
startup and inject it into endpoints.

Minimal FastAPI app
-------------------

.. code-block:: python

    from fastapi import FastAPI, HTTPException
    from smartbindb import SmartBinDB

    app = FastAPI(title="BIN Lookup")
    db = SmartBinDB()

    @app.get("/bin/{bin_value}")
    async def lookup(bin_value: str):
        result = await db.get_bin_info(bin_value)
        if result["status"] != "SUCCESS":
            raise HTTPException(status_code=404, detail=result["message"])
        return result["data"][0]

Bank search endpoint
--------------------

.. code-block:: python

    @app.get("/bank/{name}")
    async def by_bank(name: str, limit: int = 25):
        return await db.get_bins_by_bank(name, limit=limit)

Country listing endpoint
------------------------

.. code-block:: python

    @app.get("/country/{code}")
    async def by_country(code: str, limit: int = 100):
        return await db.get_bins_by_country(code, limit=limit)

Lifespan management
-------------------

If you prefer the lifespan pattern, build the database during startup:

.. code-block:: python

    from contextlib import asynccontextmanager
    from fastapi import FastAPI
    from smartbindb import SmartBinDB

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.db = SmartBinDB()
        yield

    app = FastAPI(lifespan=lifespan)

    @app.get("/bin/{bin_value}")
    async def lookup(request, bin_value: str):
        return await request.app.state.db.get_bin_info(bin_value)
