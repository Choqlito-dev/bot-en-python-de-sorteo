import discord
from discord.ext import commands
import json

class Leaderboard(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='leaderboard')
    async def leaderboard(self, ctx):
        with open('economy.json', 'r') as f:
            data = json.load(f)
        
        sorted_data = sorted(data.items(), key=lambda x: x[1].get('balance', 0), reverse=True)
        leaderboard = "\n".join([f"<@{user_id}>: {info['balance']} monedas" for user_id, info in sorted_data[:10]])

        await ctx.send(f"**Ranking de monedas:**\n{leaderboard}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Leaderboard(bot))
