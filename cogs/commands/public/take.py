import discord
from discord.ext import commands
import json

class Take(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.language_cog = bot.get_cog('Language')  # Obtén el *cog* Language

    @commands.command(name='take')
    @commands.has_permissions(administrator=True)
    async def take(self, ctx, member: discord.Member, amount: int):
        if amount <= 0:
            if self.language_cog:
                message = self.language_cog.get_translation(ctx.guild.id, 'amount_positive')
            else:
                message = "La cantidad debe ser positiva."
            await ctx.send(message)
            return

        receiver_id = str(member.id)

        with open('economy.json', 'r') as f:
            data = json.load(f)

        if receiver_id not in data or data[receiver_id].get('balance', 0) < amount:
            if self.language_cog:
                message = self.language_cog.get_translation(ctx.guild.id, 'insufficient_balance')
            else:
                message = "Este usuario no tiene suficiente saldo para quitar esta cantidad."
            await ctx.send(message)
            return

        data[receiver_id]['balance'] -= amount

        with open('economy.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        if self.language_cog:
            message = self.language_cog.get_translation(ctx.guild.id, 'took_money').format(amount, member.mention)
        else:
            message = f"Se han quitado {amount} monedas a {member.mention}"

        await ctx.send(message)

async def setup(bot: commands.Bot):
    await bot.add_cog(Take(bot))
