import discord
from discord.ext import commands
import json

class History(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.language_cog = bot.get_cog('Language')  # Obtén el *cog* Language

    @commands.command(name='history')
    async def history(self, ctx):
        user_id = str(ctx.author.id)
        try:
            with open('transactions.json', 'r') as f:
                transactions = json.load(f)
            
            user_transactions = transactions.get(user_id, [])
            if not user_transactions:
                if self.language_cog:
                    message = self.language_cog.get_translation(ctx.guild.id, 'no_transactions')
                else:
                    message = "No tienes transacciones registradas."
                await ctx.send(message)
                return

            history_message = self.language_cog.get_translation(ctx.guild.id, 'transaction_history')
            for transaction in user_transactions:
                history_message += f"{transaction}\n"

            await ctx.send(history_message)

        except FileNotFoundError:
            if self.language_cog:
                message = self.language_cog.get_translation(ctx.guild.id, 'no_file')
            else:
                message = "No se ha encontrado el archivo de transacciones."
            await ctx.send(message)

async def setup(bot: commands.Bot):
    await bot.add_cog(History(bot))
