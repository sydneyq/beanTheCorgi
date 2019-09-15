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

class Event(commands.Cog):

    def __init__(self, client, database, meta):
        self.client = client
        self.dbConnection = database
        self.meta = meta
        #self.queue = list()
        #self.tea_score = 0
        #self.coffee_score = 0

        self.strings = ['the quick brown fox jumps over the lazy dog', #1
        'bean the corgi is the goodest boy', #2
        'tea and coffee make the world go round', #3
        'with great power comes great responsibility', #4
        'elementary my dear watson', #5
        'the snack that smiles back', #6
        'take a deep breath', #7
        'sorry earth is closed today', #8
        'i am right where i am supposed to be', #9
        'houston we have a problem', #10
        'you had me at hello world', #11
        'keep your friends close and your enemies closer', #12
        'today is going to be a good day', #13
        'adventure is out there', #14
        'there is no one i would rather be than me', #15
        'hakuna matata what a wonderful phrase', #16
        'no one deserves to be forgotten', #17
        'i could do this all day', #18
        'i have been falling for thirty minutes', #19
        'come with me where dreams are born and time is never planned', #20
        'i wanna be the very best like no one ever was', #21
        'we are a product of the stories we tell ourselves', #22
        'let us learn to show our friendship for a man when he is alive and not after he is dead', #23
        'a man can learn more from defeat than success or victory', #24
        'when there are clouds in the sky you will get by', #25
        'if you do not like where you are move you are not a tree', #26
        'i think you are confused for it is you who will taste defeat', #27
        'we used google cloud platform to predict how clouds will behave', #28
        'it is bed o clock you best be sleeping', #29
        'when you cannot sleep at night it is because you are awake', #30
        'does the sun shine for man to tell it where to cast its rays',
        'the wilderness must be explored',
        'no one deserves to fade away',
        'a wilderness explorer is a friend to all be it plants or fish or tiny mole caw caw rawr']

        dirname = os.path.dirname(__file__)
        filename2 = os.path.join(dirname, 'docs/emojis.json')
        filename3 = os.path.join(dirname, 'docs/ids.json')

        with open(filename2) as json_file:
            self.emojis = json.load(json_file)

        with open(filename3) as json_file:
            self.ids = json.load(json_file)

    @commands.command(aliases=['2019'])
    async def badge2019(self, ctx):
        user = self.meta.getProfile(ctx.author)
        badges = user['badges']
        if '2019' not in badges:
            badges.append('2019')
            self.dbConnection.updateProfile({"id": ctx.author.id}, {"$set": {"badges": badges}})
            await ctx.send(embed = self.meta.embedDone())
            return
        else:
            await ctx.send(embed = self.meta.embedOops())
            return
    '''
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
    @commands.command(aliases=['typerace', 'squadrace', 'squadracer', 'race'])
    async def typeracer(self, ctx, channel: discord.TextChannel = None):#rounds: int = 1, channel: discord.TextChannel = None):
        message = ctx.message
        if not self.meta.isAdmin(message.author):
            return

        if channel is None:
            channel = ctx.channel

        await ctx.message.delete()

        #for round in range(0, rounds):
        string = random.choice(self.strings)
        amt = 25
        altered = ''

        punctuation = ['!', '@', '&', '.']
        for ch in string:
            altered += ch + random.choice(punctuation)

        altered = altered[:-1]

        embed = discord.Embed(
            title = 'Game On: Win ' + str(amt) + ' Coins!',
            #title = 'Game On: Squad Racers!',
            color = discord.Color.teal()
        )

        embed.add_field(name='Be the first to type the sentence without any punctuation or symbols!',
        value='`' + altered + '`')
        #embed.set_footer(text = 'This expires in 3 minutes.')
        await channel.send(embed = embed)

        def check(m):
            return m.content.lower() == string and m.channel == channel

        msg = await self.client.wait_for('message', check=check)

        user = self.meta.getProfile(msg.author)
        '''
        elif user['squad'] == '':
            embed = discord.Embed(
                title = 'Sorry, you\'re not in a Squad yet! Join one by using `+squad tea/coffee`.',
                color = discord.Color.teal()
            )
            await channel.send(embed = embed)
            return

        squad = user['squad']
        if user['squad'] == 'Tea':
            self.tea_score += 1
        else:
            self.coffee_score += 1
        '''
        coins = user['coins'] + amt
        self.dbConnection.updateProfile({"id": msg.author.id}, {"$set": {"coins": coins}})

        embed2 = discord.Embed(
            title = msg.author.name + ', you\'ve just earned ' + str(amt) + ' coins!',
            description = 'Your total: `' + str(coins) + '` coins',
            color = discord.Color.teal()
        )
        '''
        embed2 = discord.Embed(
            title = msg.author.name + ' just earned `1` point for **' + squad + '**!',
            description = '**Tea Squad:** `' + str(self.tea_score) + '`\n**Coffee Squad:** `' + str(self.coffee_score) + '`',
            color = discord.Color.teal()
        )
        '''
        await channel.send(embed = embed2)
        return

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if random.random() < .1:
            #check timestamp
            past_timestamp = self.dbConnection.findMeta({'id':'server'})['typerace']
            if past_timestamp == '' or self.meta.hasBeen10Minutes(past_timestamp, self.meta.getDateTime()):
                self.dbConnection.updateMeta({'id':'server'}, {'$set': {'typerace': self.meta.getDateTime()}})
                casual = 257751892241809408
                casual2 = 599757443362193408
                #casual = 593153723610693632 #cmd
                #casual2 = 593153723610693632 #cmd
                #vc_chat = 595384066618949692
                channels = [casual, casual2]
                channel = random.choice(channels)
                channel = message.guild.get_channel(channel)

                string = random.choice(self.strings)
                amt = 50
                altered = ''

                punctuation = ['!', '@', '&', '.']
                for ch in string:
                    altered += ch + random.choice(punctuation)

                altered = altered[:-1]

                embed = discord.Embed(
                    title = 'Game On: Win ' + str(amt) + ' Coins!',
                    #title = 'Game On: Squad Racers!',
                    color = discord.Color.teal()
                )

                embed.add_field(name='Be the first to type the sentence without any punctuation or symbols!',
                value='`' + altered + '`')
                await channel.send(embed = embed)

                def check(m):
                    return m.content.lower() == string and m.channel == channel

                msg = await self.client.wait_for('message', check=check)

                user = self.meta.getProfile(msg.author)

                coins = user['coins'] + amt
                self.dbConnection.updateProfile({"id": msg.author.id}, {"$set": {"coins": coins}})

                embed2 = discord.Embed(
                    title = msg.author.name + ', you\'ve just earned ' + str(amt) + ' coins!',
                    description = 'Your total: `' + str(coins) + '` coins',
                    color = discord.Color.teal()
                )

                await channel.send(embed = embed2)
                return
            else:
                return
        else:
            return

def setup(client):
    database_connection = Database()
    meta_class = Meta(database_connection)
    client.add_cog(Event(client, database_connection, meta_class))
