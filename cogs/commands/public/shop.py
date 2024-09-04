import discord
from discord.ext import commands
import json

class Shop(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='shop')
    async def shop(self, ctx):
        # Define some items for the shop
        items = {
            'item1': 100,
            'item2': 200
        }
        
        shop_message = "**Tienda:**\n"
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
            await ctx.send("Este item no está en la tienda.")
            return
        
        price = items[item]
        if balance < price:
            await ctx.send("No tienes suficiente saldo para comprar este item.")
            return

        data[user_id]['balance'] -= price
        # Here you would add the item to the user's inventory if you have an inventory system

        with open('economy.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        await ctx.send(f"Has comprado {item} por {price} monedas")

async def setup(bot: commands.Bot):
    await bot.add_cog(Shop(bot))
