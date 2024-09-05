import discord
from discord.ext import commands

class ErrorCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(
                title="The command does not exist",
                description=f"The command `{ctx.invoked_with}` Does not exist. Use a valid command.",
                color=discord.Color.blue()
            )

            await ctx.send(embed=embed)
        else:
            raise error
        
async def setup(bot):
   await bot.add_cog(ErrorCommand(bot))