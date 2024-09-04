import discord
from discord.ext import commands

# Crea una instancia del bot
intents = discord.Intents.default()
intents.message_content = True  # Habilita la lectura de contenido de mensajes (necesario para algunos comandos)

bot = commands.Bot(command_prefix="-", intents=intents)

# Evento: el bot está listo
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

# Comando simple
@bot.command(name='saludar')
async def saludar(ctx):
    await ctx.send(f'¡Hola, {ctx.author.name}!')

# Iniciar el bot con el token
bot.run('MTI3OTYzNjIyNTEyMDI3MjQ2NQ.GDmtnb.W4WsI6UHcZxNInHagqC9w9Fe_EhZmWxQ2kftyM')


