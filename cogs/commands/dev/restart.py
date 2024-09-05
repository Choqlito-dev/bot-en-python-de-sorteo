import discord
from discord.ext import commands
import os
import sys

class Restart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["r"])
    @commands.is_owner()
    async def restart(self, ctx):
        await ctx.send("Reiniciando el bot...")
        await self.bot.close()
        os.execv(sys.executable, ['python'] + sys.argv)

async def setup(bot):
    await bot.add_cog(Restart(bot))
