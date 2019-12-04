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

    #rules, rules, rules
    @commands.Cog.listener()
    async def on_message(self, message):
        #don't start yet
        return

        if message.author.bot:
            return

        if random.random() < .1:
            past_timestamp = self.dbConnection.findMeta({'id':'server'})['event']
            if past_timestamp == '' or self.meta.hasBeenMinutes(15, past_timestamp, self.meta.getDateTime()):
                self.dbConnection.updateMeta({'id':'server'}, {'$set': {'event': self.meta.getDateTime()}})
                channels = [257751892241809408, 599757443362193408]

                #event_channel = 593153723610693632 #cmd
                event_channel = random.choice(channels)
                channel = message.guild.get_channel(event_channel)

                num = random.randint(1, len(self.rules))
                rule = self.rules[num]

                title = 'Rules, Rules, Rules!'
                desc = 'Be the first to say the corresponding rule number to earn coins!'
                e = self.meta.embed(title, desc, 'gold')
                n = 'What `rule number` does this rule title or desciption belong to?'
                v = random.choice({rule['TITLE'], rule['DESC']})
                v = f'`{v}`'
                e.add_field(name=n, value=v)
                e.set_footer(text='Expires in 60 seconds.')
                await channel.send(embed = embed, delete_after=60)

                def check(m):
                    return m.content.lower() == str(num) and m.channel == channel

                try:
                    msg = await self.client.wait_for('message', timeout=60.0, check=check)
                except asyncio.TimeoutError:
                    return
                else:
                    amt = random.choice(25, 50, 75)
                    user = self.meta.getProfile(msg.author)

                    coins = user['coins'] + amt
                    self.dbConnection.updateProfile({"id": msg.author.id}, {"$set": {"coins": coins}})

                    embed2 = discord.Embed(
                        title = msg.author.name + ', you\'ve just earned `' + str(amt) + '` coins!',
                        description = 'Your total: `' + str(coins) + '` coins',
                        color = discord.Color.teal()
                    )

                    await channel.send(embed = embed2)
            return

def setup(client):
    database_connection = Database()
    meta_class = Meta(database_connection)
    client.add_cog(TempEvent(client, database_connection, meta_class))
