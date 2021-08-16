from asyncio import tasks
from asyncio.transports import SubprocessTransport
import requests
from requests.api import request
from config import targets, secondsBetweenChecks, CHANNEL_ID
from time import sleep
import asyncio
import os
import discord
from discord.ext import tasks

client = discord.Client()
oldValues = []


@tasks.loop(seconds=secondsBetweenChecks)
async def scanPages():
    global oldValues
    loop = asyncio.get_event_loop()
    channel = client.get_channel(CHANNEL_ID)
    for i, target in enumerate(targets):
        oldScan = oldValues[i]
        futureResponse = loop.run_in_executor(None, requests.get, target)
        response = await futureResponse
        content = str(response.content.decode())
        if content != oldScan:
            print("DIFFERENT CONTENT DETECTED FOR " + target)
            oldValues[i] = content
            msg = "@everyone Change Detected on " + target + ": "+ content
            await channel.send(msg[:1900]) # if message too long it gets only the last 1900 symbols, you set it to :1900 to get the first 1900
        else:
            print("SAME CONTENT DETECTED FOR " + target + " skipping...")

for target in targets:
    oldValues.append("")

@client.event
async def on_ready():    
    scanPages.start()

client.run(os.getenv('BOTTOKEN'))
