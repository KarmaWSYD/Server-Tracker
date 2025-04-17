# Server-Tracker
Python-based discord bot for tracking Steam game servers using A2S. Includes optional code to send commands to servers via pterodactyl API.

Requires configuration, including Discord application token, Discord channel ID (for sending the server list), configuring each tracked server as well as optionally pterodactyl panel details. Both the example.env as well as the server_tracker_config.json file need to be edited.

This code is provided as-is without any explicit or implicit warranties.

Config explanation:
{
    "IP": "IP or FQDN here", <---- add the IP or FQDN for the servers
    "Servers": {},  <---- comma-separated key-value pairs where the key is a port and value is a server code (required to be set but can be any text)
    "discord_channel_id": 0, <---- id of the discord channel
    "discord_message_id": 0, <---- id of the message to edit
    "Server_Name": "Server Name here", <---- server name to be set in the embed
    "Ad": [], <---- list of strings, each one is a command to be sent to the servers in srvlist
    "srvlist":[] <---- list of pterodactyl server UUIDs to send commands to
}
    