import discord
from discord.ext import commands

import json
from random import randint

import aiohttp
import asyncio
import async_timeout

import requests

class Pics(commands.Cog):
    channelID = 593153723610693632

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def dog(self, ctx):
        response = requests.get('https://dog.ceo/api/breeds/image/random')
        data = response.json()
        await ctx.message.channel.send(data['message'])

    @commands.command(pass_context=True)
    async def corgi(self, ctx):
        response = requests.get('https://dog.ceo/api/breed/corgi/images/random')
        data = response.json()
        await ctx.message.channel.send(data['message'])

    @commands.command(pass_context=True)
    async def cat(self, ctx):
        response = requests.get('https://aws.random.cat/meow')
        data = response.json()
        await ctx.message.channel.send(data['file'])

def setup(client):
    client.add_cog(Pics(client))
