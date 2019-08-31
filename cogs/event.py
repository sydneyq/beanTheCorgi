import discord
from discord.ext import commands
from database import Database
from .meta import Meta
import json
import os
import asyncio
import secret
import random

class Event(commands.Cog):

    def __init__(self, client, database, meta):
        self.client = client
        self.dbConnection = database
        self.meta = meta
        self.queue = list()
        self.tea_score = 0
        self.coffee_score = 0

    @commands.command(aliases=['pts'])
    async def points(self, ctx):
        embed2 = discord.Embed(
            title = 'Squad Points',
            description = '**Tea Squad:** `' + str(self.tea_score) + '`\n**Coffee Squad:** `' + str(self.coffee_score) + '`',
            color = discord.Color.teal()
        )

        if self.tea_score > self.coffee_score:
            embed2.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/591611902459641856/613918428293627914/teamteaBean.png')
        elif self.coffee_score > self.tea_score:
            embed2.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/591611902459641856/613918442034298890/teamcoffeeBean.png')

        await ctx.send(embed = embed2)

    #karaoke event
    '''
    @commands.Cog.listener()
    async def on_message(self, message):
        if not isinstance(message.channel, discord.TextChannel):
            return

        if ('karaoke' in message.channel.name):
            id = message.author.id
            if ('add me' in message.content.lower()):
                if id not in self.queue:
                    self.queue.append(id)
                    embed = discord.Embed(
                        title = 'Added you to the queue!',
                        color = discord.Color.teal()
                    )
                    await message.channel.send(embed = embed)
                else:
                    embed = discord.Embed(
                        title = 'You\'re already in the queue!',
                        color = discord.Color.teal()
                    )
                    await message.channel.send(embed = embed)
            elif ('remove me' in message.content.lower()):
                if id in self.queue:
                    embed = discord.Embed(
                        title = 'I\'ve removed you from the queue.',
                        color = discord.Color.teal()
                    )
                    await message.channel.send(embed = embed)

                    self.queue.remove(id)
                else:
                    embed = discord.Embed(
                        title = 'You\'re not in the queue!',
                        color = discord.Color.teal()
                    )
                    await message.channel.send(embed = embed)
            elif ('queue' in message.content.lower()):
                say = ''

                for id in self.queue:
                    say += self.client.get_user(id).name + '\n'
                embed = discord.Embed(
                    title = 'Current Queue',
                    color = discord.Color.teal(),
                    description = say
                )
                await message.channel.send(embed = embed)
            elif 'skip' == message.content.lower() and ('angels' in [role.name for role in message.author.roles] or 'mechanic' in [role.name for role in message.author.roles]):
                self.queue.pop()
                embed = discord.Embed(
                    title = 'I\'ve skipped to the next person.',
                    color = discord.Color.teal()
                )
                await message.channel.send(embed = embed)
                self.queue.remove(id)
    '''

    #team names in names event
    '''
    @commands.command(aliases=['snames'])
    async def squadnames(self, ctx):
        guild = ctx.guild
        members = guild.members

        embed = discord.Embed(
            title = 'Squad Names',
            color = discord.Color.teal()
        )

        tea = 0
        teaMembers = ''
        coffee = 0
        coffeeMembers = ''

        for member in members:
            if not self.meta.isVerified(member):
                continue
            if member.nick is not None:
                if self.meta.hasWord(member.nick, 'tea'):
                    tea += 1
                    teaMembers += '<@' + str(member.id) + '>\n'
                if self.meta.hasWord(member.nick, 'coffee'):
                    coffee += 1
                    coffeeMembers += '<@' + str(member.id) + '>\n'
            else:
                if self.meta.hasWord(member.name, 'tea'):
                    tea += 1
                    teaMembers += '<@' + str(member.id) + '>\n'
                if self.meta.hasWord(member.name, 'coffee'):
                    coffee += 1
                    coffeeMembers += '<@' + str(member.id) + '>\n'

        embed.add_field(name='Members with \"tea\"', value= '`' + str(tea) + '` Members\n' + teaMembers)
        embed.add_field(name='Members with \"coffee\"', value= '`' + str(coffee) + '` Members\n' + coffeeMembers)

        await ctx.send(embed = embed)
        return
    '''
    #@commands.cooldown(1, 60*60*24, commands.BucketType.user)
    #@commands.Cog.listener()
    #@commands.cooldown(1, 180, commands.BucketType.guild)
    #async def on_message(self, message):
    @commands.command(aliases=['typerace', 'squadrace', 'squadracer', 'race'])
    async def typeracer(self, ctx, channel: discord.TextChannel = None):#rounds: int = 1, channel: discord.TextChannel = None):
        message = ctx.message
        if not self.meta.isAdmin(message.author):
            return

        if channel is None:
            channel = ctx.channel

        await ctx.message.delete()

        #corresponding arrays
        strings = ['the quick brown fox jumps over the lazy dog', #1
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
        'i have been falling for twenty minutes', #19
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
        'a wilderness explorer is a friend to all be it plants or fish or tiny mole']

        #for round in range(0, rounds):
        string = random.choice(strings)
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

        user = self.dbConnection.findProfile({'id' : msg.author.id})
        if user is None:
            embed = discord.Embed(
                title = 'Sorry, you don\'t have a profile yet! You can make one by using +profile.',
                color = discord.Color.teal()
            )
            await channel.send(embed = embed)
            return
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

    @commands.command()
    async def avatar(self, ctx, channel: discord.TextChannel = None):
        message = ctx.message
        if not self.meta.isAdmin(message.author):
            return

        if channel is None:
            channel = ctx.channel

        await ctx.message.delete()

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
            return m.content.lower() == '💥' and m.channel == channel

        cont = True

        while (cont):
            msg = await self.client.wait_for('message', check=check)

            user = self.meta.getProfile(msg.author)

            if user['squad'] == '':
                embed = discord.Embed(
                    title = 'Sorry, you\'re not in a Squad yet! Join one by using `+squad tea/coffee`.',
                    color = discord.Color.teal()
                )
                await channel.send(embed = embed)
                cont = True
                continue
            elif user['affinity'] is None or user['affinity'] == '':
                embed = discord.Embed(
                    title = 'Sorry, you haven\'t set an affinity yet! You can do that by using `+affinity fire/water/air/earth`.',
                    color = discord.Color.teal()
                )
                await channel.send(embed = embed)
                cont = True
                continue
            elif user['affinity'] != result:
                embed = discord.Embed(
                    title = 'You don\'t have the required affinity! You\'re looking for someone who\'s `' + result + '`.',
                    color = discord.Color.teal()
                )
                await channel.send(embed = embed)
                cont = True
                continue
            elif user['affinity'] == result:
                cont = False

                squad = user['squad']
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

    '''
    @commands.command(aliases=['pewpew', 'pewpewpew', 'teamwork', 'teambattle'])
    async def pew(self, ctx, channel: discord.TextChannel = None):
        message = ctx.message
        if not self.meta.isAdmin(message.author):
            return

        if channel is None:
            channel = ctx.channel

        await ctx.message.delete()

        embed = discord.Embed(
            title = 'Game On: Pewpew!',
            description = 'Get three people from your Squad to say \"pewpew\" first to gain a point!',
            color = discord.Color.teal()
        )

        await channel.send(embed = embed)

        isFull = False
        local_tea_score = 0
        local_coffee_score = 0

        tea_shooters = []
        coffee_shooters = []

        while not isFull:
            def check(m):
                return (m.content.lower() == 'pew pew' or m.content.lower() == 'pewpew') and m.channel == channel

            msg = await self.client.wait_for('message', check=check)

            user = self.dbConnection.findProfile({'id' : msg.author.id})
            if user is None:
                embed = discord.Embed(
                    title = 'Sorry, you don\'t have a profile yet! You can make one by using +profile.',
                    color = discord.Color.teal()
                )
                await channel.send(embed = embed)
                continue

            elif user['squad'] == '':
                embed = discord.Embed(
                    title = 'Sorry, you\'re not in a Squad yet! Join one by using `+squad tea/coffee`.',
                    color = discord.Color.teal()
                )
                await channel.send(embed = embed)
                continue

            squad = user['squad']

            if squad == 'Tea':
                if msg.author.id in tea_shooters:
                    embed = discord.Embed(
                        title = 'Sorry, you\'ve already shot in this round!',
                        color = discord.Color.teal()
                    )
                    await channel.send(embed = embed)
                    continue
                else:
                    tea_shooters.append(msg.author.id)

                local_tea_score += 1
            else:
                if msg.author.id in coffee_shooters:
                    embed = discord.Embed(
                        title = 'Sorry, you\'ve already shot in this round!',
                        color = discord.Color.teal()
                    )
                    await channel.send(embed = embed)
                    continue
                else:
                    coffee_shooters.append(msg.author.id)

                local_coffee_score += 1

            if local_tea_score == 3 or local_coffee_score == 3:
                isFull = True

            embed3 = discord.Embed(
                title = 'Current Attacks',
                color = discord.Color.teal()
            )

            tea_shooters_str = ''
            for shooter in tea_shooters:
                tea_shooters_str += '<@' + str(shooter) + '>\n'

            if tea_shooters_str == '':
                tea_shooters_str = 'N/A'

            embed3.add_field(name='Tea Shooters (' + str(len(tea_shooters)) + '/3)', value=tea_shooters_str)

            coffee_shooters_str = ''
            for shooter in coffee_shooters:
                coffee_shooters_str += '<@' + str(shooter) + '>\n'

            if coffee_shooters_str == '':
                coffee_shooters_str = 'N/A'

            embed3.add_field(name='Coffee Shooters (' + str(len(coffee_shooters)) + '/3)', value=coffee_shooters_str)

            await channel.send(embed = embed3)

        if local_tea_score == 3:
            self.tea_score += 1
        else:
            self.coffee_score += 1

        embed2 = discord.Embed(
            title = squad + ' Squad just earned `1` point!',
            description = '**Tea Squad:** `' + str(self.tea_score) + '`\n**Coffee Squad:** `' + str(self.coffee_score) + '`',
            color = discord.Color.teal()
        )

        await channel.send(embed = embed2)

        return
    '''

def setup(client):
    database_connection = Database()
    meta_class = Meta(database_connection)
    client.add_cog(Event(client, database_connection, meta_class))
