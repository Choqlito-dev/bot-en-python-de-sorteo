import discord
from discord.ext import commands
import json

class Balance(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.language_cog = bot.get_cog('Language')  # Obtén el *cog* Language

    @commands.command(name='balance')
    async def balance(self, ctx):
        user_id = str(ctx.author.id)
        with open('economy.json', 'r') as f:
            data = json.load(f)
        
        balance = data.get(user_id, {}).get('balance', 0)
        if self.language_cog:
            message = self.language_cog.get_translation(ctx.guild.id, 'balance').format(ctx.author.mention, balance)
        else:
            message = f"{ctx.author.mention}, tu saldo actual es: {balance} monedas"

        await ctx.send(message)

async def setup(bot: commands.Bot):
    await bot.add_cog(Balance(bot))
