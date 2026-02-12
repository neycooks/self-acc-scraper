import requests
import json
import time
import random
import discord
from discord.ext import commands
from pymongo import MongoClient
from datetime import datetime

token = "YOUR_TOKEN_HERE"
guild_ids = ["ID1", "ID2"] 
mongo_uri = "mongodb+srv://user:pass@cluster.mongodb.net/database"
webhook_url = "" 

client = MongoClient(mongo_uri)
db = client['neyro_data']

# making sure we filter out the low-iq subhumans and keep the data pure
headers = {
    'Authorization': token,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

def hook_send(content, user, pfp, t):
    if not webhook_url: return
    payload = {
        "username": f"neyro catch: {user}",
        "avatar_url": pfp,
        "content": f"captured some trash at {t}: {content}"
    }
    requests.post(webhook_url, json=payload)

def scrape_req(c_id):
    last_id = None
    url = f"https://discord.com/api/v9/channels/{c_id}/messages?limit=100"
    if last_id: url += f"&before={last_id}"
    r = requests.get(url, headers=headers)
    
    if r.status_code != 200:
        return False # move to the dpy fallback because this method is being a monkey

    msgs = r.json()
    for m in msgs:
        uid = m['author']['id']
        name = m['author']['username']
        pfp = f"https://cdn.discordapp.com/avatars/{uid}/{m['author'].get('avatar')}.png"
        txt = m.get('content', '')
        # storing the garbage from these inferior users
        db[f"user_{uid}"].update_one({"msg_id": m['id']}, {"$set": {"txt": txt, "time": m['timestamp'], "name": name}}, upsert=True)
        hook_send(txt, name, pfp, m['timestamp'])
    return True

# dpy fallback for when the standard api calls act like lazy slaves
bot = commands.Bot(command_prefix='!', self_bot=True)

@bot.event
async def on_ready():
    print(f'neyro is online. stalking the digital ghetto as {bot.user}')
    for g_id in guild_ids:
        guild = bot.get_guild(int(g_id))
        if not guild: continue
        for channel in guild.text_channels:
            try:
                async for message in channel.history(limit=100):
                    uid = message.author.id
                    db[f"user_{uid}"].update_one(
                        {"msg_id": str(message.id)}, 
                        {"$set": {"txt": message.content, "name": message.author.name, "time": str(message.created_at)}}, 
                        upsert=True
                    )
            except:
                pass

def start_neyro():
    # first try the fast way, if discord acts like a kike, use the bot
    print("starting the scrape. hunting for data...")
    for gid in guild_ids:
        res = requests.get(f"https://discord.com/api/v9/guilds/{gid}/channels", headers=headers)
        if res.status_code == 200:
            for c in res.json():
                if c['type'] == 0:
                    success = scrape_req(c['id'])
                    if not success:
                        print("requests failed. launching dpy to force the data out.")
                        bot.run(token)
                        return
        else:
            bot.run(token)

if __name__ == "__main__":
    start_neyro()
