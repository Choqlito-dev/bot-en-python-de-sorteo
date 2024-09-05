import discord
from discord.ext import commands
import os
import json
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def get_prefix(bot, message):
    """Obtiene el prefijo para el servidor actual."""
    if os.path.isfile('prefixes.json'):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
    else:
        prefixes = {}
    return prefixes.get(str(message.guild.id), "!")

bot = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.all(), help_command=None)

def load_translations():
    """Carga las traducciones desde el archivo JSON."""
    with open('translations.json', 'r', encoding='utf-8') as f:
        return json.load(f)

translations = load_translations()

def get_translation(guild_id, key):
    """Obtiene la traducción del mensaje en el idioma configurado."""
    lang = bot.cogs['Language'].get_language(guild_id)
    return translations[lang].get(key, key)

@bot.event
async def on_command_error(ctx, error):
    """Maneja los errores de comandos y envía mensajes de error traducidos."""
    error_message = str(error)
    if isinstance(error, commands.CommandNotFound):
        error_message = get_translation(ctx.guild.id, 'command_not_found')
    elif isinstance(error, commands.BadArgument):
        error_message = get_translation(ctx.guild.id, 'error_occurred')
    await ctx.send(error_message)

@bot.event
async def on_ready():
    """Carga los *cogs* y muestra un mensaje cuando el bot esté listo."""
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
    """Procesa los comandos de los mensajes no bot."""
    if not message.author.bot:
        await bot.process_commands(message)

@bot.command()
async def test(ctx):
    """Comando de prueba."""
    await ctx.send(get_translation(ctx.guild.id, 'test_message'))

TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN:
    bot.run(TOKEN)
else:
    print("No se encontró el token. Asegúrate de que el archivo .env esté configurado correctamente.")
