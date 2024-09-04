import discord
from discord.ext import commands
import json

class Give(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='give')
    @commands.has_permissions(administrator=True)
    async def give(self, ctx, member: discord.Member, amount: int):
        if amount <= 0:
            await ctx.send("La cantidad debe ser positiva.")
            return

        giver_id = str(ctx.author.id)
        receiver_id = str(member.id)

        with open('economy.json', 'r') as f:
            data = json.load(f)

        if giver_id not in data or data[giver_id].get('balance', 0) < amount:
            await ctx.send("No tienes suficiente saldo para dar esta cantidad.")
            return

        if receiver_id not in data:
            data[receiver_id] = {'balance': 0}
        
        data[giver_id]['balance'] -= amount
        data[receiver_id]['balance'] += amount

        with open('economy.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        await ctx.send(f"{ctx.author.mention} ha dado {amount} monedas a {member.mention}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Give(bot))
