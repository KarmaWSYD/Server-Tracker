# Server-Tracker
Python-based discord bot for tracking Steam game servers using A2S. Includes optional code to send commands to servers via pterodactyl API. Also tracks online users for each server as well as total servers (timestamped, data in CSV format in ./data/players.csv).

Requires configuration, including Discord application token, Discord channel ID (for sending the server list), configuring each tracked server as well as optionally pterodactyl panel details. Both the example.env as well as the main app file need to be changed for the bot to work.

This code is provided as-is without any explicit or implicit warranties.
