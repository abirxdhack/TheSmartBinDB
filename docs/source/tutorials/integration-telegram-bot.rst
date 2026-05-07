Integrating SmartBinDB with a Telegram bot
==========================================

The async surface area makes SmartBinDB a natural fit for ``aiogram``,
``python-telegram-bot`` v20+, ``pyrogram`` and ``Telethon``.

aiogram example
---------------

.. code-block:: python

    import asyncio
    from aiogram import Bot, Dispatcher, types
    from aiogram.filters import Command
    from smartbindb import SmartBinDB

    bot = Bot(token="YOUR_TOKEN")
    dp = Dispatcher()
    db = SmartBinDB()

    @dp.message(Command("bin"))
    async def bin_cmd(message: types.Message):
        parts = (message.text or "").split(maxsplit=1)
        if len(parts) < 2:
            await message.reply("Usage: /bin <6-8 digit bin>")
            return
        result = await db.aget_bin_info(parts[1].strip())
        if result["status"] != "SUCCESS":
            await message.reply(result["message"])
            return
        row = result["data"][0]
        await message.reply(
            f"<b>BIN</b> {row['bin']}\n"
            f"<b>Brand</b> {row['brand']}\n"
            f"<b>Type</b> {row['type']}\n"
            f"<b>Issuer</b> {row['issuer']}\n"
            f"<b>Country</b> {row['Country']['Name']}",
            parse_mode="HTML",
        )

    asyncio.run(dp.start_polling(bot))

pyrogram example
----------------

.. code-block:: python

    from pyrogram import Client, filters
    from smartbindb import SmartBinDB

    db = SmartBinDB()
    app = Client("smartbin-bot", bot_token="YOUR_TOKEN", api_id=1, api_hash="x")

    @app.on_message(filters.command("bin"))
    async def bin_cmd(client, message):
        if len(message.command) < 2:
            await message.reply("Usage: /bin <bin>")
            return
        result = await db.aget_bin_info(message.command[1])
        if result["status"] != "SUCCESS":
            await message.reply(result["message"])
            return
        row = result["data"][0]
        await message.reply(
            f"BIN {row['bin']} — {row['brand']} ({row['type']})\n"
            f"Issuer: {row['issuer']}\n"
            f"Country: {row['Country']['Name']}"
        )

    app.run()
