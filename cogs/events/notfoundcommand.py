import discord
from discord.ext import commands

class ErrorCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(
                title="No existe el comando",
                description=f"El comando `{ctx.invoked_with}` no existe. Por favor, usa un comando válido.",
                color=discord.Color.blue()
            )

            await ctx.send(embed=embed)
        else:
            raise error
        
async def setup(bot):
   await bot.add_cog(ErrorCommand(bot))