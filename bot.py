import discord
from discord.ext import commands
import os
import json
from dotenv import load_dotenv

load_dotenv()

def get_prefix(bot, message):
    if os.path.isfile('prefixes.json'):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
    else:
        prefixes = {}
    return prefixes.get(str(message.guild.id), "!")

bot = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Bot {bot.user} ha iniciado')
    for root, dirs, files in os.walk('./cogs'):
        for filename in files:
            if filename.endswith('.py') and filename != '__init__.py':
                cog_name = f'cogs.{os.path.relpath(os.path.join(root, filename), start="cogs").replace(os.path.sep, ".")[:-3]}'
                try:
                    await bot.load_extension(cog_name)
                    print(f'Cargado {cog_name}')
                except Exception as e:
                    print(f'Error cargando {cog_name}: {e}')

@bot.event
async def on_message(message):
    if not message.author.bot:
        await bot.process_commands(message)

@bot.command()
async def test(ctx):
    await ctx.send("hola")

TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN:
    bot.run(TOKEN)
else:
    print("No se encontró el token. Asegúrate de que el archivo .env esté configurado correctamente.")
