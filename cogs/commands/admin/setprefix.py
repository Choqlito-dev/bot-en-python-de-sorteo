import discord
from discord.ext import commands
import json
import os

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["sp", "setp"])
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx, new_prefix: str):
        # Cargar prefijos desde el archivo JSON si existe
        if os.path.isfile('prefixes.json'):
            with open('prefixes.json', 'r') as f:
                prefixes = json.load(f)
        else:
            prefixes = {}

        # Actualizar el prefijo del servidor
        prefixes[str(ctx.guild.id)] = new_prefix
        
        # Guardar los prefijos actualizados en el archivo JSON
        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f)

        await ctx.send(f"El prefijo ha sido cambiado a: `{new_prefix}`")

async def setup(bot):
    await bot.add_cog(Config(bot))
