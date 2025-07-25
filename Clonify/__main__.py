import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from Clonify import LOGGER, app, userbot
from Clonify.core.call import PRO
from Clonify.misc import sudo
from Clonify.plugins import ALL_MODULES
from Clonify.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS
from Clonify.plugins.tools.clone import restart_bots


async def init():
    if not config.STRING1:
        LOGGER(__name__).error("String Session not filled, please provide a valid session.")
        exit()

    await sudo()

    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception as e:
        LOGGER(__name__).warning(f"Failed to load banned users: {e}")

    # Start all clients
    await app.start()
    await userbot.start()
    await PRO.start()

    # Load all plugins
    for all_module in ALL_MODULES:
        importlib.import_module("Clonify.plugins" + all_module)

    LOGGER("Clonify.plugins").info("✅ All Features Loaded Successfully!")

    # Start streaming
    try:
        await PRO.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("Clonify").error(
            "❌ Please start a voice chat in your log group/channel before starting the bot."
        )
        exit()
    except Exception as e:
        LOGGER("Clonify").warning(f"Stream failed: {e}")

    await PRO.decorators()
    await restart_bots()

    LOGGER("Clonify").info(
        "╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎ MADE BY NOBITA ☠︎︎\n╚═════ஜ۩۞۩ஜ════╝"
    )

    # Keep the bot running
    await idle()

    # On stop, close everything cleanly
    await app.stop()
    await userbot.stop()
    await PRO.stop()
    LOGGER("Clonify").info("🛑 Music Bot Stopped.")


if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init())
