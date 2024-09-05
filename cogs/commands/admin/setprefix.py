import discord
from discord.ext import commands
import json
import os

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.language_cog = bot.get_cog('Language')  # Obtén el *cog* Language

    @commands.command(aliases=["sp", "setp"])
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx, new_prefix: str):
        """Cambia el prefijo del bot para el servidor actual."""
        if os.path.isfile('prefixes.json'):
            with open('prefixes.json', 'r') as f:
                prefixes = json.load(f)
        else:
            prefixes = {}

        prefixes[str(ctx.guild.id)] = new_prefix
        
        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, ensure_ascii=False, indent=4)

        # Obtén el mensaje traducido
        if self.language_cog:
            message = self.language_cog.get_translation(ctx.guild.id, 'prefix_changed').format(new_prefix)
        else:
            message = f"El prefijo ha sido cambiado a: `{new_prefix}`"

        await ctx.send(message)

async def setup(bot):
    await bot.add_cog(Config(bot))
