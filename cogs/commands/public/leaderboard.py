import discord
from discord.ext import commands
import json

class Leaderboard(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.language_cog = bot.get_cog('Language')  # Obtén el *cog* Language

    @commands.command(name='leaderboard')
    async def leaderboard(self, ctx):
        with open('economy.json', 'r') as f:
            data = json.load(f)
        
        sorted_data = sorted(data.items(), key=lambda x: x[1].get('balance', 0), reverse=True)
        leaderboard = "\n".join([f"<@{user_id}>: {info['balance']} monedas" for user_id, info in sorted_data[:10]])

        if self.language_cog:
            message = self.language_cog.get_translation(ctx.guild.id, 'leaderboard').format(leaderboard)
        else:
            message = f"**Ranking de monedas:**\n{leaderboard}"

        await ctx.send(message)

async def setup(bot: commands.Bot):
    await bot.add_cog(Leaderboard(bot))
