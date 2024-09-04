import discord
from discord.ext import commands
import json

class Balance(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='balance')
    async def balance(self, ctx):
        user_id = str(ctx.author.id)
        with open('economy.json', 'r') as f:
            data = json.load(f)
        
        balance = data.get(user_id, {}).get('balance', 0)
        await ctx.send(f"{ctx.author.mention}, tu saldo actual es: {balance} monedas")

async def setup(bot: commands.Bot):
    await bot.add_cog(Balance(bot))
