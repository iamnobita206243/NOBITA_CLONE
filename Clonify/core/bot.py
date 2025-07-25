from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus

import config
from ..logging import LOGGER


class PRO(Client):
    def __init__(self):
        LOGGER(__name__).info("Starting Bot...")
        super().__init__(
            name="Clonify",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()

        self.id = self.me.id
        self.name = self.me.first_name + (" " + self.me.last_name if self.me.last_name else "")
        self.username = self.me.username
        self.mention = self.me.mention

        try:
            await self.send_message(
                chat_id=config.LOGGER_ID,
                text=(
                    f"<u><b>» {self.mention} Bot Started :</b></u>\n\n"
                    f"🆔 ID : <code>{self.id}</code>\n"
                    f"👤 Name : {self.name}\n"
                    f"🔗 Username : @{self.username}"
                ),
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error(
                "❌ Bot can't access log group/channel. Make sure you've added the bot there."
            )
            exit()
        except Exception as ex:
            LOGGER(__name__).error(f"❌ Failed to send start message: {type(ex).__name__}")
            exit()

        try:
            a = await self.get_chat_member(config.LOGGER_ID, self.id)
            if a.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error(
                    "❌ Please promote the bot as admin in your log group/channel."
                )
                exit()
        except Exception as ex:
            LOGGER(__name__).error(f"❌ Failed to check admin status: {type(ex).__name__}")
            exit()

        LOGGER(__name__).info(f"✅ Music Bot Started as {self.name}")

    async def stop(self):
        await super().stop()
        LOGGER(__name__).info("🛑 Bot stopped cleanly.")
