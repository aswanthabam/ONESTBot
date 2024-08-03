from decouple import config
from discord import app_commands
from discord.ext.commands import Cog
import re
import io
from bot import CustomBot
import discord
from utils.types import Role, Channel

log_path = config("LOG_PATH")

class UserCog(Cog):

    def __init__(self, bot: CustomBot) -> None:
        self.bot = bot

    @app_commands.command(name="error-log", description="download error log")
    @app_commands.checks.has_any_role(Role.ADMINS.value, Role.APPRAISER.value, Role.BOT_DEV.value)
    @app_commands.describe(date="Date of the log in the format 'YYYY-MM-DD'", clear="Clear all existing logs")
    async def error_log(self, interaction: discord.Interaction, date: str = None, clear: bool = False):
        await interaction.response.send_message(content='Check your Direct messages',
                                                ephemeral=True, delete_after=5)
        path = f"{log_path}/error.log"
        if date:
            logs = []
            with open(path, 'r') as file:
                lines = file.readlines()

            for line in lines:
                if match := re.search(
                        r'\[(\d{4}-\d{2}-\d{2}) \d{2}:\d{2}:\d{2}\]', line
                ):
                    if match[1] >= date:
                        logs.append(line)
                        logs.extend(lines[lines.index(line) + 1:])
                        break
            log = ''.join(logs)
            log_file = io.BytesIO(log.encode())
            return await interaction.user.send(file=discord.File(log_file, f"{date}_error.log"))

        with open(path, 'rb') as file:
            await interaction.user.send(file=discord.File(file, 'error.log'))
        if clear:
            with open(path, 'w'):
                pass

    @error_log.error
    async def permission_error(self, interaction: discord.Interaction, error: Exception):
        if isinstance(error, app_commands.MissingAnyRole):
            await interaction.response.send_message(content='You do not have permission to use this command',
                                                    ephemeral=True, delete_after=5)
        elif isinstance(error, app_commands.NoPrivateMessage):
            channels = await self.bot.guild.fetch_channels()
            lobby = discord.utils.get(channels, name=Channel.LOBBY.value)
            await interaction.response.send_message(
                f"You can't use this command in DM. You can use this in {lobby.mention}.", ephemeral=True)
        else:
            raise error


async def setup(bot: CustomBot) -> None:
    """Add the Example cog to the bot tree"""
    await bot.add_cog(UserCog(bot))
