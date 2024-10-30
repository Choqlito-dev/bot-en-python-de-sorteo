import discord
from discord.ext import commands
from ..utils.giveaway_utils import load_giveaways, save_giveaways, parse_time
import time

class StartGiveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="gstart")
    @commands.has_permissions(manage_guild=True)
    async def gstart(self, ctx, tiempo: str, ganadores: int, *, premio: str):
        """Inicia un nuevo sorteo"""
        try:
            # Convertir tiempo a segundos
            tiempo_total = parse_time(tiempo)
            
            # Calcular timestamp final
            end_timestamp = int(time.time() + tiempo_total)

            embed = discord.Embed(
                title="🎉 SORTEO 🎉",
                description=f"Premio: {premio}\n"
                           f"Ganadores: {ganadores}\n"
                           f"Termina: <t:{end_timestamp}:R>\n\n"
                           f"Reacciona con 🎉 para participar!",
                color=0x2f3136  # Color gris oscuro como Apollo
            )
            embed.set_footer(text=f"Organizado por: {ctx.author.name}")
            
            message = await ctx.send(embed=embed)
            await message.add_reaction("🎉")
            
            giveaways = load_giveaways()
            giveaways[str(message.id)] = {
                "premio": premio,
                "ganadores": ganadores,
                "end_time": end_timestamp,
                "channel_id": ctx.channel.id,
                "guild_id": ctx.guild.id,
                "host_id": ctx.author.id
            }
            save_giveaways(giveaways)
            
        except ValueError as e:
            await ctx.send(f"Error: {e}. Usa el formato correcto, por ejemplo `1m`, `2h`, `1d`.")

async def setup(bot):
    await bot.add_cog(StartGiveaway(bot))