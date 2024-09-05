import discord
from discord.ext import commands
import json

class Shop(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.language_cog = bot.get_cog('Language')  # Obtén el *cog* Language

    @commands.command(name='shop')
    async def shop(self, ctx):
        items = {
            'item1': 100,
            'item2': 200
        }
        
        shop_message = self.language_cog.get_translation(ctx.guild.id, 'shop')
        for item, price in items.items():
            shop_message += f"{item}: {price} monedas\n"

        await ctx.send(shop_message)

    @commands.command(name='buy')
    async def buy(self, ctx, item: str):
        items = {
            'item1': 100,
            'item2': 200
        }

        with open('economy.json', 'r') as f:
            data = json.load(f)

        user_id = str(ctx.author.id)
        if user_id not in data:
            data[user_id] = {'balance': 0}
        
        balance = data[user_id].get('balance', 0)
        if item not in items:
            if self.language_cog:
                message = self.language_cog.get_translation(ctx.guild.id, 'item_not_in_shop')
            else:
                message = "Este item no está en la tienda."
            await ctx.send(message)
            return
        
        price = items[item]
        if balance < price:
            if self.language_cog:
                message = self.language_cog.get_translation(ctx.guild.id, 'insufficient_balance')
            else:
                message = "No tienes suficiente saldo para comprar este item."
            await ctx.send(message)
            return

        data[user_id]['balance'] -= price
        # Aquí añadirías el item al inventario del usuario si tienes un sistema de inventario

        with open('economy.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        if self.language_cog:
            message = self.language_cog.get_translation(ctx.guild.id, 'bought_item').format(item, price)
        else:
            message = f"Has comprado {item} por {price} monedas"

        await ctx.send(message)

async def setup(bot: commands.Bot):
    await bot.add_cog(Shop(bot))
