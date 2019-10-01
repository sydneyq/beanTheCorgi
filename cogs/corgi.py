import discord
from discord.ext import commands
from database import Database
from .meta import Meta
import json
import os
import asyncio
import secret
import random
from numpy.random import choice

class Corgi(commands.Cog):

    def __init__(self, client, database, meta):
        self.client = client
        self.dbConnection = database
        self.meta = meta

        dirname = os.path.dirname(__file__)
        filename2 = os.path.join(dirname, 'docs/emojis.json')
        filename3 = os.path.join(dirname, 'docs/ids.json')
        filename4 = os.path.join(dirname, 'docs/corgi.json')

        with open(filename2) as json_file:
            self.emojis = json.load(json_file)

        with open(filename3) as json_file:
            self.ids = json.load(json_file)

        with open(filename4) as json_file:
            self.corgi = json.load(json_file)

    @commands.command(aliases=['c'])
    async def corgi(self, ctx, corgi = None):
        corgi = corgi.capitalize()
        isTea = True
        user = self.meta.getProfile(ctx.author)
        if corgi is None or not(corgi == 'Mocha' or corgi == 'Matcha'):
            if user['squad'] == '':
                await ctx.send(embed = self.meta.embedOops())
            else:
                if user['squad'] != 'Tea':
                    isTea = False
                    corgi = 'Mocha'
                else:
                    corgi = 'Matcha'
                await ctx.send(embed = self.embedCorgi(user['squad']))
        else:
            await ctx.send(embed = self.embedCorgi(corgi))

    def getCorgi(self, corgi):
        corgi = self.dbConnection.findMeta({"id": corgi})
        return corgi

    def embedCorgi(self, corgi):
        corgi = self.getCorgi(corgi)
        str = ''

        embed2 = discord.Embed(
            title = 'Squad Listeners',
            color = discord.Color.teal()
        )

        embed2.add_field(name=self.emojis['Tea'] + ' Tea Squad `('+str(tea_num)+')`',value=tea_names)
        embed2.add_field(name=self.emojis['Coffee'] + ' Coffee Squad `('+str(coffee_num)+'`)',value=coffee_names)

        if tea_num > coffee_num:
            embed2.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/591611902459641856/613918428293627914/teamteaBean.png')
        elif coffee_num > tea_num:
            embed2.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/591611902459641856/613918442034298890/teamcoffeeBean.png')
            
        return embed


def setup(client):
    database_connection = Database()
    meta_class = Meta(database_connection)
    client.add_cog(Corgi(client, database_connection, meta_class))
