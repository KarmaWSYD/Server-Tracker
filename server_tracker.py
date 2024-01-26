
import time
start = time.perf_counter()
import asyncio
from steam import SteamQuery
from dotenv import load_dotenv
import os
import discord
from discord import app_commands
from discord.ext import tasks
from datetime import datetime
import csv
# Code used for sending messages to gameservers using pterodactyl API.
# Uncomment and configure in order to use.
#from pydactyl import PterodactylClient
#import random


def query(ip: str, port: int):
    server_obj = SteamQuery(ip, port)
    return_dictionary = server_obj.query_server_info()
    return return_dictionary

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    async def setup_hook(self):
        await self.tree.sync()


intents = discord.Intents.default()
client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')
    end = time.perf_counter()
    print(f"Loaded Server Details Bot in {end-start:0.4f} seconds")
    await loopdeloop()
    
@tasks.loop(seconds=5)
async def loopdeloop():
        try:
            os.mkdir("./data")
        except FileExistsError:
            pass
        t = 0
        tu = 0
        tempv = 0
        
        load_dotenv()
        chid = int(os.getenv("CHANNEL")) # Channel ID
        channel = client.get_channel(chid)
        # Code used for sending messages to gameservers using pterodactyl API.
        # Uncomment and configure in order to use.
        #apipass = os.getenv("PTERO_TOKEN") # Client API token, obtainable through the pterodactyl panel
        #site = os.getenv("PANEL") # panel address
        #api = PterodactylClient(site, apipass)
        #srvlist = ["server1", "server2"] # comma-separated list of server UUID strings, UUIDs obtainable using the pterodactyl panel
        count = 0
        maxcount = 0
        embedVar = discord.Embed(title=titles, description=f"", color=0x336EFF, timestamp= datetime.utcnow())
        serverlist = {port : server_code, port2 : server_code} # separated list of ports (int) and server codes (int, set server code as None if nonexistent.)
        srvdata = {}
        srvdata.update({"time":datetime.now().strftime(f'%Y-%m-%d %H:%M:%S')})
        ip = "sub.domain.tld" # SET IPv4 OR FQDN of the server
        titles = f"Servers, currently online: `{count}` players"
        for key in serverlist:
            try:
                dictquery = query(ip, key)
                count += dictquery["players"]
                maxcount += dictquery["max_players"]
                embedVar.add_field(name=f"{dictquery['name']} Players: {dictquery['players']}/{dictquery['max_players']}", value=f"IP: `{ip}` Port`: `{key}`, Server Code: `{serverlist.get(key)}`", inline=False)
                srvdata.update({dictquery['name']:dictquery['players']})
                
            except KeyError:
                pass
        srvdata.update({"total":count})
        message = await channel.send(embed=embedVar)
        while True:
            start = time.perf_counter()
            if os.path.isfile(f"./data/players.csv") == False:
                with open(f"./data/players.csv", "w", newline="") as csvfile:
                    w = csv.DictWriter(csvfile, fieldnames=srvdata.keys())
                    w.writeheader()
                    w.writerow(srvdata)
            else:
                with open(f"./data/players.csv", "a", newline="") as csvfile:
                    w = csv.DictWriter(csvfile, fieldnames=srvdata.keys())
                    w.writerow(srvdata)
            await asyncio.sleep(3)
            # Code used for sending messages to gameservers using pterodactyl API.
            # Uncomment and configure in order to use.
            #tempv += 1
            #if tempv % 80 == 0:
            #    r = random.randint(0, 2)
            #    if r == 0:
            #        msg = "do something" # command inside this string is sent to all servers in srvlist.
            #    elif r == 1:
            #        msg = " do something else"
            #    elif r == 2:
            #        msg = "do another thing"
            #    for server in srvlist:
            #        api.client.servers.send_console_command(server_id=server, cmd=msg)
            count = 0
            maxcount = 0
            embedVar = discord.Embed(title=titles, description=f"Playtime: `{(t/86400):0.2f}` days since last restart, bot uptime: `{(tu/86400):0.2f}` days.", color=0x336EFF)
            for key in serverlist:
                try:
                    dictquery = query(ip, key)
                    count += dictquery["players"]
                    maxcount += dictquery["max_players"]
                    embedVar.title=titles
                    embedVar.color=0x336EFF
                    embedVar.timestamp=datetime.utcnow()
                    embedVar.add_field(name=f"{dictquery['name']} Players: {dictquery['players']}/{dictquery['max_players']}", value=f"IP: `{ip}` Port: `{key}`, Server Code: `{serverlist.get(key)}`", inline=False)
                    srvdata.update({dictquery['name']:dictquery['players']})
                except KeyError:
                    embedVar.title=titles
                    embedVar.color=0xFF0000
                    embedVar.timestamp=datetime.utcnow()
                    embedVar.add_field(name=f"Server Offline", value=f"IP: `{ip}` Port: `{key}`, Server Code: `{serverlist.get(key)}`", inline=False)
                    
            srvdata.update({"total":count})
            srvdata.update({"time":datetime.now().strftime(f'%Y-%m-%d %H:%M:%S')})
            end = time.perf_counter()
            t +=(end-start)*count
            tu +=(end-start)
            await message.edit(embed=embedVar)
                
            
load_dotenv()
token = os.getenv("DISCORD_TOKEN")
client.run(token)
