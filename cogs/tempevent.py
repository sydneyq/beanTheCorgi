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

class TempEvent(commands.Cog):

    def __init__(self, client, database, meta):
        self.client = client
        self.dbConnection = database
        self.meta = meta
        self.tea_score = 0
        self.coffee_score = 0

        dirname = os.path.dirname(__file__)
        filename2 = os.path.join(dirname, 'docs/emojis.json')
        filename3 = os.path.join(dirname, 'docs/ids.json')

        with open(filename2) as json_file:
            self.emojis = json.load(json_file)

        with open(filename3) as json_file:
            self.ids = json.load(json_file)
    '''
    @commands.command(aliases=['changepts', 'changept', 'chpts', 'chpt'])
    async def changePoints(self, ctx, squad, pts:int):
        if not self.meta.isBotOwner(ctx.author):
            return
        else:
            if squad == 'Coffee':
                self.coffee_score = pts
            elif squad == 'Tea':
                self.tea_score = pts
            await ctx.send(embed = self.meta.embedDone())

    @commands.command(aliases=['pts'])
    async def points(self, ctx):
        embed2 = discord.Embed(
            title = 'Squad Points',
            description = self.emojis['Tea'] + ' **Tea Squad:** `' + str(self.tea_score) + '`\n' + self.emojis['Coffee'] + ' **Coffee Squad:** `' + str(self.coffee_score) + '`',
            color = discord.Color.teal()
        )

        if self.tea_score > self.coffee_score:
            embed2.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/591611902459641856/613918428293627914/teamteaBean.png')
        elif self.coffee_score > self.tea_score:
            embed2.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/591611902459641856/613918442034298890/teamcoffeeBean.png')

        await ctx.send(embed = embed2)
    '''
    @commands.command(aliases=['pts', 'points'])
    async def listeners(self, ctx):
        tea_num = 0
        tea_names = ''
        coffee_num = 0
        coffee_names = ''

        tea = self.getNum(ctx, 'Tea')
        tea_num = tea['num']
        tea_names = tea['names']

        coffee = self.getNum(ctx, 'Coffee')
        coffee_num = coffee['num']
        coffee_names = coffee['names']

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

        await ctx.send(embed = embed2)

    def getNum(self, ctx, squad):
        num = 0
        names = ''
        profiles = self.dbConnection.findProfiles({'squad' : squad})
        for doc in profiles:
            id = doc['id']
            user = ctx.guild.get_member(id)
            if user is None:
                self.dbConnection.removeProfile({"id": id})
                return
            if 'Listeners' in [role.name for role in user.roles]:
                num += 1
                names += '<@' + str(user.id) + '>, '

        names = names[:len(names) - 2]
        stats = {
            "num":num,
            "names":names
        }
        return stats


def setup(client):
    database_connection = Database()
    meta_class = Meta(database_connection)
    client.add_cog(TempEvent(client, database_connection, meta_class))
