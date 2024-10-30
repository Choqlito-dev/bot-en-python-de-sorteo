import discord
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["p", "lt", "Ping"])
    async def ping(self, ctx):
        await ctx.send("¡Pong!")

async def setup(bot):
    await bot.add_cog(Ping(bot))
