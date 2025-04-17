
import time
start = time.perf_counter()
import asyncio
from steam import SteamQuery # pip install SteamQuery
from dotenv import load_dotenv
import os, json, random
import discord
from discord import app_commands
from discord.ext import tasks
from datetime import datetime, timezone, timedelta
from pydactyl import PterodactylClient
from asyncdactyl import AsyncDactyl
from discord_webhook import AsyncDiscordWebhook, DiscordEmbed # pip install discord-webhook

class data():
    srvtime = {}
    t = 0 # playtime counter
    tu = 0 # uptime counter
    start = time.perf_counter() # used for calculating playtime and uptime between loop executions
    serverlist = {} # dict of key-value pairs of server ports and server codes
    discord_channel_id = 0
    discord_message_id = 0
    server_name = "Server Name"
    ip = "127.0.0.1"
    ad = []
    srvlist = []

def query(ip: str, port: int):
    server_obj = SteamQuery(ip, port)
    return_dictionary = server_obj.query_server_info()
    return return_dictionary

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)


# Has to be in code for on_ready() to work
intents = discord.Intents.default()
client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')    
    update_list.start()
    ad.start()
    end = time.perf_counter()
    print(f"Loaded Server Details Bot in {end-start:0.4f} seconds")
        
        
async def update_max_players(server, current_players: int, max_players: int):
    newplayers = max_players
    if current_players >= 20 and max_players == 24:
        newplayers = 36
    elif current_players < 18 and max_players > 24:
        newplayers = 24
    elif current_players >= 30 and max_players == 36:
        newplayers = 48
    elif current_players < 28 and max_players > 36:
        newplayers = 36
    elif current_players >= 40 and max_players == 48:
        newplayers = 60
    elif current_players < 38 and max_players > 48:
        newplayers = 48
    elif current_players >= 50 and max_players == 60:
        newplayers = 72
    elif current_players < 48 and max_players > 60:
        newplayers = 60
    elif current_players >= 60 and max_players == 72:
        newplayers = 80
    elif current_players < 58 and max_players > 72:
        newplayers = 72
    elif current_players >= 70 and max_players == 80:    
        newplayers = 100
    elif current_players < 68 and max_players > 80:
        newplayers = 80
    
    
    if max_players != newplayers:
        await AsyncDactyl.AsyncMaxPlayers(server, newplayers)
        embed = DiscordEmbed()
        embed.set_title(title=f"Changed Player slots from {max_players} to {newplayers}")
        embed.set_author(name=f"{await AsyncDactyl.AsyncGetServerName(server=server[0])}")
        embed.color = 0x00ffff
        webhook = AsyncDiscordWebhook(url=os.getenv("SERVER_LOGS_WEBHOOK"))
        webhook.add_embed(embed=embed)
        await webhook.execute()

@tasks.loop(minutes=10)
async def ad():
    if data.srvlist != [] and data.ad != []:
        apipass = os.getenv("PTERO_TOKEN")
        site = os.getenv("PANEL")
        api = PterodactylClient(site, apipass)
        msg = random.choice(data.ad)
        for server in data.srvlist:
            try:
                api.client.servers.send_console_command(server_id=server, cmd=msg)
            except Exception as e:
                print(f"Error sending command to server {server}: {e}")


@tasks.loop(minutes=2)
async def update_list():
    start = data.start
    serverlist = data.serverlist
    channel_id = client.get_channel(data.discord_channel_id)
    msgs = await channel_id.fetch_message(data.discord_message_id)
    oldembed: discord.Embed = msgs.embeds[0]
    embedVar = discord.Embed(color=0x336EFF)
    count = 0
    
    b = 0 # used to keep  track of which server is being queried
    for key in serverlist:
        dictquery = query(data.ip, int(key))
        if dictquery['online']:
            count += dictquery["players"]
            players = dictquery["players"]
            maxplayers = dictquery["max_players"]
            embedVar.add_field(name=f"{dictquery['name']} Players: {players}/{maxplayers}", value=f"IP: `{data.ip}` Port: `{key}`, Server Code: `{serverlist.get(key)}`", inline=False)
            if data.srvlist != []:             
                await update_max_players(server=[f"{data.srvlist[b]}"], current_players=players, max_players=maxplayers)
        b+=1 # increment server counter
    
    end = time.perf_counter()
    
    data.t +=(end-start)*count # bot playtime counter
    data.tu +=(end-start) # bot uptime counter
    data.start = end # reset start time for next loop
    
    embedVar.title=f"{data.server_name} Servers: `{count}` players"
    embedVar.timestamp=datetime.now(timezone.utc)
    embedVar.description = f"Playtime: `{(data.t/86400):0.1f}` days since last restart, bot uptime: `{(data.tu/86400):0.1f}` days."
    
    embedfieldcounter = 0
    embedfieldchanged = False
    for i in oldembed.fields:
        if i.name != embedVar.fields[embedfieldcounter].name:
            embedfieldchanged = True
            break
        embedfieldcounter += 1
    
    if embedfieldchanged == True or (embedVar.timestamp - oldembed.timestamp) > timedelta(minutes=10):
        await msgs.edit(embed=embedVar)
    
if __name__ == "__main__":   
    with open("./server_tracker_config.json", "r") as f:
        tdata = json.load(f)
        data.serverlist = tdata['Servers'] # list of key-value pairs of server ports and server codes
        data.discord_channel_id = tdata['discord_channel_id']
        data.discord_message_id = tdata['discord_message_id'] # discord
        data.server_name = tdata['Server_Name'] # server name to be displayed in the discord embed
        data.ip = tdata['IP'] # server's IP address, can be FQDN
        data.ad = tdata['Ad'] # list of ads sent to servers
        data.srvlist = tdata['srvlist'] # used for sending commands to servers

    load_dotenv()
    token = os.getenv("DISCORD_TOKEN")
    client.run(token)
