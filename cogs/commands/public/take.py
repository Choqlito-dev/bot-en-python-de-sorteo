import discord
from discord.ext import commands
import json

class Take(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='take')
    @commands.has_permissions(administrator=True)
    async def take(self, ctx, member: discord.Member, amount: int):
        if amount <= 0:
            await ctx.send("La cantidad debe ser positiva.")
            return

        receiver_id = str(member.id)

        with open('economy.json', 'r') as f:
            data = json.load(f)

        if receiver_id not in data or data[receiver_id].get('balance', 0) < amount:
            await ctx.send("Este usuario no tiene suficiente saldo para quitar esta cantidad.")
            return

        data[receiver_id]['balance'] -= amount

        with open('economy.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        await ctx.send(f"Se han quitado {amount} monedas a {member.mention}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Take(bot))
