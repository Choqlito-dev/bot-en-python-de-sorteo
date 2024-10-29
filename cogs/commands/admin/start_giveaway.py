import discord
from discord.ext import commands
from ..utils.giveaway_utils import load_giveaways, save_giveaways, parse_time
import datetime

class StartGiveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="gstart")
    @commands.has_permissions(manage_guild=True)
    async def gstart(self, ctx, tiempo: str, ganadores: int, *, premio: str):
        """Inicia un nuevo sorteo"""
        tiempo_total = parse_time(tiempo)
        end_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=tiempo_total)
        
        embed = discord.Embed(
            title="🎉 SORTEO 🎉",
            description=f"**Premio:** {premio}\n"
                       f"**Ganadores:** {ganadores}\n"
                       f"**Termina:** <t:{int(end_time.timestamp())}:R>\n\n"
                       "Reacciona con 🎉 para participar!",
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Organizado por: {ctx.author.name}")
        
        message = await ctx.send(embed=embed)
        await message.add_reaction("🎉")
        
        giveaways = load_giveaways()
        giveaways[str(message.id)] = {
            "premio": premio,
            "ganadores": ganadores,
            "end_time": end_time.timestamp(),
            "channel_id": ctx.channel.id,
            "guild_id": ctx.guild.id,
            "host_id": ctx.author.id
        }
        save_giveaways(giveaways)

async def setup(bot):
    await bot.add_cog(StartGiveaway(bot))
