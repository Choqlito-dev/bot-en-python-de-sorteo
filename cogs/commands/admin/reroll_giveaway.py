import discord
from discord.ext import commands
from ..utils.giveaway_utils import load_giveaways, select_winners

class RerollGiveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="greroll")
    @commands.has_permissions(manage_guild=True)
    async def greroll(self, ctx, message_id: str):
        """Vuelve a elegir ganadores para un sorteo terminado"""
        giveaways = load_giveaways()
        
        try:
            message = await ctx.channel.fetch_message(int(message_id))
            data = giveaways.get(message_id, {})
            winners = await select_winners(message, data.get("ganadores", 1))
            
            if winners is None:
                return await ctx.send("No hay participantes válidos para reelegir.")
                
            winner_mentions = ", ".join(winner.mention for winner in winners)
            await ctx.send(f"🎉 Nuevos ganadores: {winner_mentions}")
            
        except Exception as e:
            await ctx.send("No pude encontrar ese sorteo o ya no está disponible.")

async def setup(bot):
    await bot.add_cog(RerollGiveaway(bot))
