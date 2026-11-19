import logging

import discord
from discord import app_commands
from discord.ext import commands

from methin.config import Settings
from methin.db import check_connection, make_engine, make_session_factory

log = logging.getLogger("methin")


class MethinBot(commands.Bot):
    def __init__(self, settings: Settings) -> None:
        # Komendy slash nie wymagają intentu message_content
        super().__init__(command_prefix=commands.when_mentioned, intents=discord.Intents.default())
        self.settings = settings
        self.engine = make_engine(settings.database_url)
        self.session_factory = make_session_factory(self.engine)

    async def setup_hook(self) -> None:
        await check_connection(self.engine)
        log.info("Połączono z bazą danych")

        # Tu będą ładowane kolejne moduły (cogs): postac, walka, ekwipunek, rynek, etc.
        self.tree.add_command(app_commands.Command(name="ping", description="Sprawdza, czy Methin żyje", callback=_ping))

        if self.settings.dev_guild_id:
            guild = discord.Object(id=self.settings.dev_guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        else:
            await self.tree.sync()

    async def close(self) -> None:
        await self.engine.dispose()
        await super().close()


async def _ping(interaction: discord.Interaction) -> None:
    await interaction.response.send_message("Pong! Methin działa.", ephemeral=True)
