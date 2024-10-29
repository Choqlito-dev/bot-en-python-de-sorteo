import discord
from discord.ext import commands
from ..utils.giveaway_utils import load_giveaways, save_giveaways, select_winners

class EndGiveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="gend")
    @commands.has_permissions(manage_guild=True)
    async def gend(self, ctx, message_id: str):
        """Termina un sorteo inmediatamente"""
        giveaways = load_giveaways()
        
        if message_id not in giveaways:
            return await ctx.send("Ese sorteo no existe o ya terminó.")
            
        try:
            message = await ctx.channel.fetch_message(int(message_id))
            data = giveaways[message_id]
            winners = await select_winners(message, data["ganadores"])
            
            if winners is None:
                return await ctx.send(f"No se pudo determinar un ganador para el sorteo de {data['premio']}!")
                
            winner_mentions = ", ".join(winner.mention for winner in winners)
            
            embed = discord.Embed(
                title="🎉 SORTEO TERMINADO 🎉",
                description=f"**Premio:** {data['premio']}\n"
                           f"**Ganadores:** {winner_mentions}\n",
                color=discord.Color.green()
            )
            embed.set_footer(text="Sorteo terminado")
            
            await message.edit(embed=embed)
            await message.channel.send(f"¡Felicitaciones {winner_mentions}! Ganaste: **{data['premio']}**")
            
            del giveaways[message_id]
            save_giveaways(giveaways)
            
        except Exception as e:
            await ctx.send("No pude encontrar ese mensaje de sorteo.")

async def setup(bot):
    await bot.add_cog(EndGiveaway(bot))
