import discord
from discord.ext import commands
import json
import os

class Register(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.language_cog = bot.get_cog('Language')  # Obtén el *cog* Language

    @commands.command(name='register')
    async def register(self, ctx):
        user_id = str(ctx.author.id)

        if not os.path.exists('economy.json'):
            with open('economy.json', 'w') as f:
                json.dump({}, f)

        with open('economy.json', 'r') as f:
            data = json.load(f)

        if user_id in data:
            if self.language_cog:
                message = self.language_cog.get_translation(ctx.guild.id, 'already_registered')
            else:
                message = "Ya estás registrado en el sistema de economía."
            await ctx.send(message)
            return

        data[user_id] = {'balance': 500}

        with open('economy.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        if self.language_cog:
            message = self.language_cog.get_translation(ctx.guild.id, 'registered').format(ctx.author.mention)
        else:
            message = f"{ctx.author.mention} ha sido registrado con un saldo inicial de 500 monedas."

        await ctx.send(message)

async def setup(bot: commands.Bot):
    await bot.add_cog(Register(bot))
