import discord
import os
from discord.ext import commands

import sys
import signal
import asyncio
import pymongo
import math

import database
import secret

client = commands.Bot(commands.when_mentioned_or('+'), case_insensitive=True)

@client.event
async def on_ready():
    print('Bean is online!')
    await client.change_presence(status=discord.Status.online, activity=discord.Game('DM me for help/feedback!'))
'''
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(
            title = "Cooldown: please retry in `{}s`.".format(math.ceil(error.retry_after)),
            color = discord.Color.teal()
        )
        await ctx.send(embed = embed, delete_after=10)
'''
@client.command()
async def reload(ctx, extension):
    if ctx.message.author.id == secret.BOT_OWNER_ID:
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        await ctx.send('Cog reloaded!')
    else:
        await ctx.send('You don\'t have the permissions to do that!')

@client.command()
async def load(ctx, extension):
    if ctx.message.author.id == secret.BOT_OWNER_ID:
        client.load_extension(f'cogs.{extension}')
        await ctx.send('Cog loaded!')
    else:
        await ctx.send('You don\'t have the permissions to do that!')

@client.command()
async def unload(ctx, extension):
    if ctx.message.author.id == secret.BOT_OWNER_ID:
        client.unload_extension(f'cogs.{extension}')
        await ctx.send('Cog unloaded!')
    else:
        await ctx.send('You don\'t have the permissions to do that!')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(secret.BOT_TOKEN)
