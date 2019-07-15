import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix = '=')

MY_ID = 212723958313779201
BOT_TOKEN = 'NDMyMDM4Mzg5NjYzOTI0MjI1.XRrsHA.vvYZtBgWNB3wH1Kp5LXn_hV6MUc'

@client.event
async def on_ready():
    print('Bean is online!')

@client.command()
async def reload(ctx, extension):
    if ctx.message.author.id == MY_ID:
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        await ctx.send('Cog reloaded!')
    else:
        await ctx.send('You don\'t have the permissions to do that!')

@client.command()
async def load(ctx, extension):
    if ctx.message.author.id == MY_ID:
        client.load_extension(f'cogs.{extension}')
        await ctx.send('Cog loaded!')
    else:
        await ctx.send('You don\'t have the permissions to do that!')

@client.command()
async def unload(ctx, extension):
    if ctx.message.author.id == MY_ID:
        client.unload_extension(f'cogs.{extension}')
        await ctx.send('Cog unloaded!')
    else:
        await ctx.send('You don\'t have the permissions to do that!')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(BOT_TOKEN)
