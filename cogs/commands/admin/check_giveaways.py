import discord
from discord.ext import commands, tasks
from cogs.commands.utils.giveaway_utils import load_giveaways, save_giveaways, select_winners
import datetime

class CheckGiveaways(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_giveaways.start()

    @tasks.loop(seconds=30)
    async def check_giveaways(self):
        current_time = datetime.datetime.utcnow().timestamp()
        giveaways = load_giveaways()
        to_end = []
        
        for giveaway_id, data in giveaways.items():
            if current_time >= data["end_time"]:
                try:
                    channel = self.bot.get_channel(data["channel_id"])
                    if channel:
                        message = await channel.fetch_message(int(giveaway_id))
                        winners = await select_winners(message, data["ganadores"])
                        
                        if winners:
                            winner_mentions = ", ".join(winner.mention for winner in winners)
                        
                        # Calcular el tiempo desde el inicio del sorteo hasta el final
                        start_time = data.get("start_time")
                        if start_time:
                            duration_text = f"Duración: <t:{start_time}:R> hasta <t:{data['end_time']}:R>"
                        else:
                            duration_text = "Duración no disponible."

                        # Embed para el sorteo terminado
                        embed = discord.Embed(
                            title="🎉 SORTEO TERMINADO 🎉",
                            description=f"**Premio:** {data['premio']}\n"
                                        f"**Ganadores:** {winner_mentions}\n"
                                        f"{duration_text}",
                            color=discord.Color.green()
                        )
                        embed.set_footer(text="Sorteo terminado")
                        
                        await message.edit(embed=embed)
                        await channel.send(f"¡Felicitaciones {winner_mentions}! Ganaste: **{data['premio']}**")
                        
                except Exception as e:
                    print(f"Error al procesar el sorteo {giveaway_id}: {e}")
                finally:
                    to_end.append(giveaway_id)
        
        for giveaway_id in to_end:
            del giveaways[giveaway_id]
        if to_end:
            save_giveaways(giveaways)

    @check_giveaways.before_loop
    async def before_check_giveaways(self):
        await self.bot.wait_until_ready()

    def cog_unload(self):
        self.check_giveaways.cancel()

async def setup(bot):
    await bot.add_cog(CheckGiveaways(bot))
