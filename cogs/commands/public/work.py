import discord
from discord.ext import commands
import json
import random

class Work(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.language_cog = bot.get_cog('Language')  # Obtén el *cog* Language

    @commands.command(name='work')
    async def work(self, ctx):
        earnings = random.randint(50, 200)  # Ganancias aleatorias entre 50 y 200 monedas

        user_id = str(ctx.author.id)

        with open('economy.json', 'r') as f:
            data = json.load(f)

        if user_id not in data:
            data[user_id] = {'balance': 0}
        
        data[user_id]['balance'] += earnings

        with open('economy.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        if self.language_cog:
            message = self.language_cog.get_translation(ctx.guild.id, 'worked').format(earnings)
        else:
            message = f"{ctx.author.mention} ha trabajado y ha ganado {earnings} monedas."

        await ctx.send(message)

async def setup(bot: commands.Bot):
    await bot.add_cog(Work(bot))
