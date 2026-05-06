Integrating SmartBinDB with Django
==================================

Use SmartBinDB from Django's async views (Django 4.1+) or wrap it in
``async_to_sync`` from ``asgiref`` for sync views.

Async view
----------

.. code-block:: python

    from django.http import JsonResponse
    from smartbindb import SmartBinDB

    db = SmartBinDB()

    async def bin_view(request, bin_value):
        result = await db.get_bin_info(bin_value)
        return JsonResponse(result)

Sync view via async_to_sync
---------------------------

.. code-block:: python

    from asgiref.sync import async_to_sync
    from django.http import JsonResponse
    from smartbindb import SmartBinDB

    db = SmartBinDB()

    def bin_view(request, bin_value):
        result = async_to_sync(db.get_bin_info)(bin_value)
        return JsonResponse(result)

URL routing
-----------

.. code-block:: python

    from django.urls import path
    from .views import bin_view

    urlpatterns = [
        path("bin/<str:bin_value>/", bin_view),
    ]

Caching with django-cachalot or per-view cache
-----------------------------------------------

Because SmartBinDB lookups are already in-memory, you usually do not need
Django-level cache. If you want to amortize the JSON serialization cost,
use Django's per-view cache decorator on read-only endpoints.
