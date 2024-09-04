import discord
from discord.ext import commands
import json

class History(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='history')
    async def history(self, ctx):
        user_id = str(ctx.author.id)
        try:
            with open('transactions.json', 'r') as f:
                transactions = json.load(f)
            
            user_transactions = transactions.get(user_id, [])
            if not user_transactions:
                await ctx.send("No tienes transacciones registradas.")
                return

            history_message = "**Historial de transacciones:**\n"
            for transaction in user_transactions:
                history_message += f"{transaction}\n"

            await ctx.send(history_message)

        except FileNotFoundError:
            await ctx.send("No se ha encontrado el archivo de transacciones.")

async def setup(bot: commands.Bot):
    await bot.add_cog(History(bot))
