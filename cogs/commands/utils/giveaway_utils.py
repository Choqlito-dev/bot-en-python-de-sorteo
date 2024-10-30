import json
import os
import discord
import random
from typing import List, Optional

def load_giveaways() -> dict:
    """Cargar sorteos desde el archivo JSON."""
    try:
        with open('data/giveaways.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_giveaways(giveaways: dict) -> None:
    """Guardar sorteos en el archivo JSON."""
    if not os.path.exists('data'):
        os.makedirs('data')
    
    with open('data/giveaways.json', 'w') as f:
        json.dump(giveaways, f)

def parse_time(time_str: str) -> int:
    """
    Convertir un string de tiempo a segundos.
    """
    time_str = time_str.strip().lower()
    
    time_conversion = {
        "s": 1,
        "m": 60,
        "h": 3600,
        "d": 86400
    }
    
    if len(time_str) < 2:
        raise ValueError("Formato de tiempo inválido")
    
    try:
        amount = int(time_str[:-1])
        unit = time_str[-1]
    except ValueError:
        raise ValueError("El valor del tiempo debe ser un número")
    
    if unit not in time_conversion:
        raise ValueError("Unidad de tiempo no válida. Usa 's', 'm', 'h' o 'd'.")
    
    if amount <= 0:
        raise ValueError("El tiempo debe ser mayor a 0")
    
    return amount * time_conversion[unit]

async def select_winners(message: discord.Message, winner_count: int) -> Optional[List[discord.User]]:
    """Seleccionar ganadores de un sorteo."""
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