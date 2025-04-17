import asyncio
import aiohttp
import json
from dotenv import load_dotenv
import os
import time

class AsyncDactyl():
    load_dotenv() ### DO NOT REMOVE
    site = os.getenv("PANEL")
    apipass = os.getenv("PTERO_TOKEN")
    ServerNameCache = {}
    
    async def AsyncGetServerName(server):
        if server in AsyncDactyl.ServerNameCache.keys():
            if AsyncDactyl.ServerNameCache[server]['time'] + 43200 > time.time():
                return AsyncDactyl.ServerNameCache[server]['name']

        client_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {AsyncDactyl.apipass}",
                }    
        async with aiohttp.ClientSession(headers=client_headers) as session:
            async with session.get(f'{AsyncDactyl.site}/api/client/servers/{server}') as response:
                name = json.loads(await response.text())['attributes']['name']
                AsyncDactyl.ServerNameCache.update({server: {'name': name, 'time': time.time()}})
                return json.loads(await response.text())['attributes']['name']
                    
        
        
    async def AsyncMaxPlayers(servers: list, maxplayers: int):
        loop = asyncio.get_event_loop()
        tasks = []
        client_headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {AsyncDactyl.apipass}",
                    }
        
        async def ttask(srv):
                async with aiohttp.ClientSession(headers=client_headers) as session:
                    async with session.post(f'{AsyncDactyl.site}/api/client/servers/{srv}/command', data=json.dumps({"command": f"MaxPlayers {maxplayers}"})) as response:
                        if response.status != 204:
                            print(response.status)
        for server in servers:
            tasks.append(loop.create_task(ttask(server)))

        await asyncio.gather(*tasks)