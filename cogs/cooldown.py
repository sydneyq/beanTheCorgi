import discord
from discord.ext import commands
from database import Database
from .meta import Meta
import random
import json
import os
import asyncio
from numpy.random import choice
import secret

class Cooldown(commands.Cog):

    def __init__(self, client, database, meta):
        self.client = client
        self.dbConnection = database
        self.meta = meta

        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'docs/store.json')

        with open(filename) as json_file:
            self.store = json.load(json_file)

    @commands.cooldown(1, 60*60*24, commands.BucketType.user)
    @commands.command(aliases=['treasurehunt', 'treasure'])
    async def daily(self, ctx):
        id = ctx.message.author.id

        user = self.dbConnection.findProfile({"id": id})

        if user is None:
            embed = discord.Embed(
                title = 'Sorry, you don\'t have a profile yet! You can make one by using +profile.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

        companion = user['companion']
        if companion == '':
            embed = discord.Embed(
                title = 'Sorry, you need a companion for that!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

        special = False
        elements = [10, 25, 50, 75]
        weights = [0.3, 0.4, 0.2, 0.1]

        if companion in [item['name'] for item in self.store['Special Companions']]:
            special = True
            weights = [0.1, 0.3, 0.4, 0.2]
        elif companion in [item['name'] for item in self.store['Evolved Companions']]:
            special = True
            weights = [0.1, 0.3, 0.4, 0.2]

        amt = choice(elements, p=weights)

        coins = user['coins']
        coins = coins + int(amt)
        self.dbConnection.updateProfile({"id": id}, {"$set": {"coins": coins}})

        print('making embed')
        embed = discord.Embed(
            title = ctx.author.name + ', your ' + companion + ' found `' + str(amt) + '` coins!',
            description = '<@' + str(id) + '> coin count: `' + str(coins) + '`',
            color = discord.Color.teal()
        )

        print('checking url')
        if companion != '':
            isFound = False
            for c in self.store['Coin Companions']:
                if c['name'].lower() == companion.lower():
                    embed.set_image(url = c['src'])
                    isFound = True
                    break

            if not isFound:
                for c in self.store['Helped Companions']:
                    if c['name'].lower() == companion.lower():
                        embed.set_image(url = c['src'])
                        isFound = True
                        break

            if not isFound:
                for c in self.store['Special Companions']:
                    if c['name'].lower() == companion.lower():
                        embed.set_image(url = c['src'])
                        isFound = True
                        break

            if not isFound:
                for c in self.store['Evolved Companions']:
                    if c['name'].lower() == companion.lower():
                        embed.set_image(url = c['src'])
                        isFound = True
                        break

        print('is special')
        if special:
            embed.set_footer(text = 'Special Companion detected! You have a higher chance of getting more coins.')
        print('sending embed')
        await ctx.channel.send(embed = embed)

def setup(client):
    database_connection = Database()
    meta_class = Meta()
    client.add_cog(Cooldown(client, database_connection, meta_class))
