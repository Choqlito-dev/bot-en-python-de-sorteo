import discord
from discord.ext import commands
import json

class Language(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.translations = self.load_translations()
        self.languages = self.load_languages()

    def load_translations(self):
        with open('translations.json', 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_languages(self):
        try:
            with open('languages.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_languages(self):
        with open('languages.json', 'w', encoding='utf-8') as f:
            json.dump(self.languages, f, ensure_ascii=False, indent=4)

    def get_language(self, guild_id):
        return self.languages.get(str(guild_id), 'es')

    def get_translation(self, guild_id, key):
        lang = self.get_language(guild_id)
        return self.translations[lang].get(key, key)

    @commands.command(name='setlanguage')
    async def set_language(self, ctx, language):
        """Cambia el idioma del bot en el servidor."""
        if language not in self.translations:
            await ctx.send("Idioma no soportado. Usa `es` para español, `en` para inglés o `pt` para portugués.")
            return
        
        self.languages[str(ctx.guild.id)] = language
        self.save_languages()
        await ctx.send(self.get_translation(ctx.guild.id, 'language_changed'))

    @commands.command(name='greet')
    async def greet(self, ctx):
        """Saludo en el idioma configurado."""
        await ctx.send(self.get_translation(ctx.guild.id, 'greeting'))

    @commands.command(name='help')
    async def help_command(self, ctx):
        """Mensaje de ayuda en el idioma configurado."""
        await ctx.send(self.get_translation(ctx.guild.id, 'help_message'))

async def setup(bot):
    await bot.add_cog(Language(bot))
