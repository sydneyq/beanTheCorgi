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

    #unscramble
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if random.random() < .1:
            past_timestamp = self.dbConnection.findMeta({'id':'server'})['event']
            if past_timestamp == '' or self.meta.hasBeenMinutes(6, past_timestamp, self.meta.getDateTime()):
                self.dbConnection.updateMeta({'id':'server'}, {'$set': {'event': self.meta.getDateTime()}})
                #event_channel = 593153723610693632 #cmd
                event_channel = 623746736677978133
                channel = message.guild.get_channel(event_channel)

                words = ['trillion',
                'winter',
                'replacement',
                'mountain',
                'wondrous',
                'training',
                'pouring',
                'tailgate',
                'expressive',
                'frightened',
                'laughable',
                'updated',
                'frying',
                'lioness',
                'australia',
                'headphones',
                'flipper',
                'thousand',
                'swirl',
                'megabyte',
                'spiritual',
                'golfing',
                'specified',
                'journalism',
                'environmental',
                'network',
                'language',
                'koala',
                'memorization',
                'sunken',
                'airplane',
                'malibu',
                'identical',
                'temperate',
                'challenger',
                'complicated',
                'spelling',
                'painter',
                'universal',
                'director',
                'trance',
                'telekinesis',
                'index',
                'attempt',
                'rainforest',
                'conductor',
                'electric',
                'wellfare',
                'greeting',
                'acrylic',
                'bandage',
                'skies',
                'autumn']

                word = random.choice(words).lower()

                def scramble(string):
                    str = string
                    scrambled = ''

                    while len(str) > 0:
                        ch = random.randrange(len(str))
                        ch = str[ch]
                        scrambled += ch
                        str = str.replace(ch, '', 1)

                    return scrambled

                embed = discord.Embed(
                    title = 'Game On: Unscramble!',
                    color = discord.Color.teal()
                )

                scrambled = scramble(word)

                embed.add_field(name=scrambled,
                value='Unscramble the word above and say it first to win a point for your Squad!')
                embed.set_footer(text='Expires in 5 minutes.')
                await channel.send(embed = embed, delete_after=300)

                def check(m):
                    return m.content.lower() == word and m.channel == channel

                cont = True
                while (cont):
                    try:
                        msg = await self.client.wait_for('message', timeout=300.0, check=check)
                    except asyncio.TimeoutError:
                        return
                    else:
                        user = self.meta.getProfile(msg.author)
                        squad = user['squad']

                        if squad == '':
                            embed2 = discord.Embed(
                                title = msg.author.name + ', you\'re not in a Squad yet!',
                                color = discord.Color.teal()
                            )
                            await channel.send(embed = embed2, delete_after=60)
                            continue
                        elif squad == 'Tea':
                            self.tea_score += 1
                        elif squad == 'Coffee':
                            self.coffee_score += 1

                        embed = discord.Embed(
                            title = msg.author.name + ' just earned `1` point for ' + squad + '!',
                            description = '**Tea Squad:** `' + str(self.tea_score) + '`\n**Coffee Squad:** `' + str(self.coffee_score) + '`',
                            color = discord.Color.teal()
                        )

                        await channel.send(embed = embed)
                        cont = False
                        return
            return

def setup(client):
    database_connection = Database()
    meta_class = Meta(database_connection)
    client.add_cog(TempEvent(client, database_connection, meta_class))
