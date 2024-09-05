import discord
from discord.ext import commands
import json

class Transfer(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.language_cog = bot.get_cog('Language')  # Obtén el *cog* Language

    @commands.command(name='transfer')
    async def transfer(self, ctx, member: discord.Member, amount: int):
        if amount <= 0:
            if self.language_cog:
                message = self.language_cog.get_translation(ctx.guild.id, 'amount_positive')
            else:
                message = "La cantidad debe ser positiva."
            await ctx.send(message)
            return

        sender_id = str(ctx.author.id)
        receiver_id = str(member.id)

        with open('economy.json', 'r') as f:
            data = json.load(f)

        if sender_id not in data or data[sender_id].get('balance', 0) < amount:
            if self.language_cog:
                message = self.language_cog.get_translation(ctx.guild.id, 'insufficient_balance')
            else:
                message = "No tienes suficiente saldo para transferir esta cantidad."
            await ctx.send(message)
            return

        if receiver_id not in data:
            data[receiver_id] = {'balance': 0}
        
        data[sender_id]['balance'] -= amount
        data[receiver_id]['balance'] += amount

        with open('economy.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        if self.language_cog:
            message = self.language_cog.get_translation(ctx.guild.id, 'transferred_money').format(amount, member.mention)
        else:
            message = f"{ctx.author.mention} ha transferido {amount} monedas a {member.mention}"

        await ctx.send(message)

async def setup(bot: commands.Bot):
    await bot.add_cog(Transfer(bot))
