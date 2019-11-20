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

    #on-message avatar
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if isinstance(message.channel, discord.DMChannel):
            return

        if random.random() < .1:
            past_timestamp = self.dbConnection.findMeta({'id':'server'})['event']
            if past_timestamp == '' or self.meta.hasBeenMinutes(10, past_timestamp, self.meta.getDateTime()):
                self.dbConnection.updateMeta({'id':'server'}, {'$set': {'event': self.meta.getDateTime()}})
                channels = [257751892241809408, 599757443362193408, 595384066618949692]
                channel = message.guild.get_channel(random.choice(channels))

                embed = discord.Embed(
                    title = 'Game On: Avatar!',
                    description = 'Bean is the Avatar and needs teachers from each element!',
                    color = discord.Color.teal()
                )

                choices = ['Water', 'Air', 'Fire', 'Earth']
                result = random.choice(choices)
                pic = ''

                if result == 'Water':
                    pic = 'http://dpegb9ebondhq.cloudfront.net/product_photos/15204550/water-01_large.jpg'
                elif result == 'Air':
                    pic = 'https://d3u67r7pp2lrq5.cloudfront.net/product_photos/15204511/air-01_original.jpg'
                elif result == 'Fire':
                    pic = 'https://dzasv7x7a867v.cloudfront.net/product_photos/15204544/Fire-01_original.jpg'
                elif result == 'Earth':
                    pic = 'http://d3u67r7pp2lrq5.cloudfront.net/product_photos/15204526/earth-01_400w.jpg'

                embed.add_field(name='Affinity: ' + result, value='Get someone from your Squad with the correct Affinity to post the 💥 emoji before the other Squad to gain a point!')
                embed.set_thumbnail(url = pic)
                await channel.send(embed = embed)

                def check(m):
                    return '💥' in m.content.lower() and m.channel == channel

                cont = True
                while (cont):
                    msg = await self.client.wait_for('message', check=check)
                    user = self.meta.getProfile(msg.author)
                    squad = user['squad']
                    affinity = user['affinity']

                    if squad == '' or squad == 'Squadless' or squad == 'Admin':
                        await channel.send(embed = self.meta.embedOops('You don\'t have an elligible Squad!'))
                        continue
                    elif affinity is None or affinity == '' or affinity != result:
                        await channel.send(embed = self.meta.embedOops('You don\'t have the right Affinity!'))
                        continue
                    else:
                        cont = False

                        #staff temp squads
                        if self.meta.isStaff(msg.author):
                            temp_squads = self.dbConnection.findMeta({'id':'temp_squads'})
                            if msg.author.id in temp_squads['Tea']:
                                squad = 'Tea'
                            else:
                                squad = 'Coffee'

                        if squad == 'Tea':
                            self.tea_score += 1
                        else:
                            self.coffee_score += 1

                        embed2 = discord.Embed(
                            title = msg.author.name + ' just earned `1` point for ' + squad + '!',
                            description = '**Tea Squad:** `' + str(self.tea_score) + '`\n**Coffee Squad:** `' + str(self.coffee_score) + '`',
                            color = discord.Color.teal()
                        )

                        if self.tea_score > self.coffee_score:
                            embed2.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/591611902459641856/613918428293627914/teamteaBean.png')
                        elif self.coffee_score > self.tea_score:
                            embed2.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/591611902459641856/613918442034298890/teamcoffeeBean.png')


                        await channel.send(embed = embed2)

                        return

def setup(client):
    database_connection = Database()
    meta_class = Meta(database_connection)
    client.add_cog(TempEvent(client, database_connection, meta_class))
