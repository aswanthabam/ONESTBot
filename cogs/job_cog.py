from discord import app_commands
from discord.ext.commands import Cog
from bot import CustomBot
import discord

JOBS = [
    {
        'role': 'software engineer',
        'company': 'Google',
        'location': 'Mountain View, CA',
        'description': 'We are looking for a software engineer to join our team'
    },
    {
        'role': 'data scientist',
        'company': 'Facebook',
        'location': 'Menlo Park, CA',
        'description': 'We are looking for a data scientist to join our team'
    },
    {
        'role': 'product manager',
        'company': 'Amazon',
        'location': 'Seattle, WA',
        'description': 'We are looking for a product manager to join our team'

    }
]


class JobCog(Cog):

    def __init__(self, bot: CustomBot) -> None:
        self.bot = bot

    @app_commands.command(name="jobs", description="Find Jobs")
    @app_commands.describe(role="Role to search for")
    async def job_search(self, interaction: discord.Interaction, role: str):
        role = role.lower()
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send("<:onest:1269217759674503209> Searching for jobs", ephemeral=True)
        embeds = []
        for job in JOBS:
            if role == job['role']:
                embed = discord.Embed(title=f"{job['role']} at {job['company']}",
                                      description=job['description'],
                                      color=discord.Color.blue())
                embed.add_field(name="Location", value=job['location'])
                embeds.append(embed)
        if len(embeds) > 0:
            return await interaction.followup.send(embeds=embeds, ephemeral=True)
        await interaction.followup.send(content='No job found', ephemeral=True)


async def setup(bot: CustomBot) -> None:
    """Add the Example cog to the bot tree"""
    await bot.add_cog(JobCog(bot))
