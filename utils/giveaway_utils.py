import json
import discord
import random
from datetime import datetime, timedelta

def load_giveaways():
    try:
        with open('data/giveaways.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_giveaways(giveaways):
    with open('data/giveaways.json', 'w') as f:
        json.dump(giveaways, f)

def parse_time(time_str):
    time_conversion = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    return int(time_str[:-1]) * time_conversion[time_str[-1]]

async def select_winners(message, winner_count):
    reaction = discord.utils.get(message.reactions, emoji="🎉")
    if not reaction:
        return None
    
    users = []
    async for user in reaction.users():
        if not user.bot:
            users.append(user)
            
    if len(users) < winner_count:
        winner_count = len(users)
        
    if len(users) == 0:
        return None
        
    return random.sample(users, winner_count)