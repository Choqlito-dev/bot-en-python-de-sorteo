import discord
from discord.ext import commands
import json
import os

class Register(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='register')
    async def register(self, ctx):
        user_id = str(ctx.author.id)

        # Verifica si el archivo de datos existe
        if not os.path.exists('economy.json'):
            with open('economy.json', 'w') as f:
                json.dump({}, f)

        # Cargar datos
        with open('economy.json', 'r') as f:
            data = json.load(f)

        # Verifica si el usuario ya está registrado
        if user_id in data:
            await ctx.send("Ya estás registrado en el sistema de economía.")
            return

        # Registrar al usuario y asignar monedas iniciales
        data[user_id] = {'balance': 500}

        # Guardar datos
        with open('economy.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        await ctx.send(f"{ctx.author.mention} ha sido registrado con un saldo inicial de 500 monedas.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Register(bot))
