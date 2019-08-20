import discord
from discord.ext import commands
from database import Database
from .meta import Meta
import json
import os
import asyncio
import random

class Profile(commands.Cog):

    def __init__(self, client, database, meta):
        self.client = client
        self.dbConnection = database
        self.meta = meta

        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'docs/store.json')

        with open(filename) as json_file:
            self.store = json.load(json_file)

    @commands.command(aliases=['squads', 's', 'sq', 'leaderboard'])
    async def squadCount(self, ctx):
        embed = discord.Embed(
            title = 'Squad Count',
            color = discord.Color.teal()
        )

        #tea
        #total members
        tea = self.dbConnection.findProfiles({'squad' : 'Tea'})
        teaMembers = tea.count()

        #total helped
        teaHelped = 0

        #top squad member
        teaTop = ''
        teaTopHelped = 0

        for doc in tea:
            teaHelped += doc['helped']
            if doc['helped'] > teaTopHelped:
                teaTop = '<@' + str(doc['id']) + '> (' + str(doc['helped']) + ')'
                teaTopHelped = doc['helped']
            elif doc['helped'] == teaTopHelped:
                teaTop += '\n<@' + str(doc['id']) + '> (' + str(doc['helped']) + ')'

        teaStr = '`' + str(teaMembers) + '` Members\n`' + str(teaHelped) + '` Helped\nMost Helpful Member(s):\n' + teaTop

        #coffee
        #tea
        #total members
        coffee = self.dbConnection.findProfiles({'squad' : 'Coffee'})
        coffeeMembers = coffee.count()

        #total helped
        coffeeHelped = 0

        #top squad member
        coffeeTop = ''
        coffeeTopHelped = 0

        for doc in coffee:
            coffeeHelped += doc['helped']
            if doc['helped'] > coffeeTopHelped:
                coffeeTop = '<@' + str(doc['id']) + '> (' + str(doc['helped']) + ')'
                coffeeTopHelped = doc['helped']
            elif doc['helped'] == coffeeTopHelped:
                coffeeTop += '\n<@' + str(doc['id']) + '> (' + str(doc['helped']) + ')'

        coffeeStr = '`' + str(coffeeMembers) + '` Members\n`' + str(coffeeHelped) + '` Helped\nMost Helpful Member(s):\n' + coffeeTop

        #emojis
        teaName = 'Tea Squad '
        coffeeName = 'Coffee Squad '

        if teaMembers > coffeeMembers:
            teaName = teaName + '🙌🏻'
        elif teaMembers < coffeeMembers:
            coffeeName = coffeeName + '🙌🏻'

        if teaHelped > coffeeHelped:
            teaName = teaName + '🏆'
        elif teaHelped < coffeeHelped:
            coffeeName = coffeeName + '🏆'


        embed.add_field(name=teaName,value=teaStr)
        embed.add_field(name=coffeeName,value=coffeeStr, inline=False)

        await ctx.send(embed = embed)
        return

    @commands.command()
    async def squad(self, ctx, *, squad = None):
        if squad is None or (squad.lower() != 'coffee' and squad.lower() != 'tea'):
            embed = discord.Embed(
                description = 'Correct Usage: `+squad coffee` or `+squad tea`.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return
        squad = squad.lower()
        # see whats in the message -> adjust the specific persons profile based  on it
        # .update "updates" the profile $ must be used to keep old items
        id = ctx.author.id
        #user = self.dbConnection.findProfile({"id": id})
        user = self.dbConnection.findProfile({"id": id})
        print('Finding profile...')
        if user is None:
            self.dbConnection.insertProfile({'id': id, 'squad': '', 'helped': 0, 'coins': 50, 'companion': '', 'spouse': 0})
            user = self.dbConnection.findProfile({"id": id})
            print('No profile found. Creating new one...')

        print('Finding squad...')
        if user['squad'] == "Tea":
            embed = discord.Embed(
                title = 'You\'re already part of the Tea Squad!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return
        elif user['squad'] == "Coffee":
            embed = discord.Embed(
                title = 'You\'re already part of the Coffee Squad!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return
        else:
            if 'tea' in squad:
                self.dbConnection.updateProfile({"id": id}, {"$set": {"squad": "Tea"}})
                embed = discord.Embed(
                    title = 'You\'ve joined the Tea Squad!',
                    color = discord.Color.teal()
                )
                await ctx.send(embed = embed)
                role = ctx.guild.get_role(612788003542401035)
                await ctx.author.add_roles(role)
                return
            elif 'coffee' in squad:
                self.dbConnection.updateProfile({"id": id}, {"$set": {"squad": "Coffee"}})
                embed = discord.Embed(
                    title = 'You\'ve joined the Coffee Squad!',
                    color = discord.Color.teal()
                )
                await ctx.send(embed = embed)
                role = ctx.guild.get_role(612788004926521365)
                await ctx.author.add_roles(role)
                return
            else:
                embed = discord.Embed(
                    title = 'That Squad doesn\'t exist. Please choose either Coffee or Tea.',
                    color = discord.Color.teal()
                )
                await ctx.send(embed = embed)
                return

    @commands.command()
    async def getSquadRole(self, ctx):
        id = ctx.author.id
        user = self.dbConnection.findProfile({"id": id})

        if user is None:
            embed = discord.Embed(
                title = 'Sorry, you don\'t have a profile yet! You can make one by using +profile.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

        if user['squad'] == 'Coffee':
            role = ctx.guild.get_role(612788004926521365)
            await ctx.author.add_roles(role)
            embed = discord.Embed(
                title = 'Consider it done! ✅',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
        elif user['squad'] == 'Tea':
            role = ctx.guild.get_role(612788003542401035)
            await ctx.author.add_roles(role)
            embed = discord.Embed(
                title = 'Consider it done! ✅',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                title = 'Couldn\'t find your Squad.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

    #   Goes through certain elements of a users data in the database
    #   and puts them into an embed to send to the user through the bot
    @commands.command(aliases=['p'])
    async def profile(self, ctx, other: discord.Member = None):
        if other == None:
            id = ctx.author.id
        else:
            id = other.id
        #user = self.dbConnection.profileFind({"id": id})

        user = self.dbConnection.findProfile({"id": id})
        name = self.client.get_user(id).name

        if other == None:
            member = ctx.message.author
        else:
            member = other

        if user is None:
            self.dbConnection.insertProfile({'id': id, 'squad': '', 'helped': 0, 'coins': 50, 'companion': '', 'spouse': 0})
            user = self.dbConnection.findProfile({"id": id})

        pic = member.avatar_url

        #Basics
        if (user['squad'] == "Tea"):
            embed = discord.Embed(color=0xa72461)
            embed.add_field(name="Squad", value=user['squad'], inline=True)
            embed.set_author(name = name, icon_url = 'https://cdn2.stylecraze.com/wp-content/uploads/2015/04/2072_11-Surprising-Benefits-And-Uses-Of-Marijuana-Tea_shutterstock_231770824.jpg')
        elif (user['squad'] == "Coffee"):
            embed = discord.Embed(color=0x9cf196)
            embed.add_field(name="Squad", value=user['squad'], inline=True)
            embed.set_author(name = name, icon_url = 'https://www.caffesociety.co.uk/assets/recipe-images/latte-small.jpg')
        else:
            embed = discord.Embed(color = discord.Color.teal())
            embed.add_field(name="Squad", value='No Squad yet. Use `+squad tea/coffee` to join one!', inline=True)
            embed.set_author(name = name)

        embed.set_footer(text = 'Mind Café', icon_url = 'https://media.discordapp.net/attachments/591611902459641856/593267453363224588/Bean_Icon.png')

        #Marriage
        if user['spouse'] == 0:
            spouse = 'N/A'
        else:
            spouse = '<@' + str(user['spouse']) + '>'
        embed.add_field(name="Spouse", value=spouse, inline=False)

        #Achievements
        #   helped
        helped = user['helped']
        embed.add_field(name="Help Points", value=helped, inline=True)

        #   coins
        coins = user['coins']
        embed.add_field(name="Coins", value=coins, inline=True)

        #Companion
        companion = user['companion']
        msg = ''

        if companion is not '':
            isSpecial = False
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
                        isSpecial = True
                        break

            if not isFound:
                for c in self.store['Evolved Companions']:
                    if c['name'].lower() == companion.lower():
                        embed.set_image(url = c['src'])
                        isFound = True
                        isSpecial = True
                        break

            msg = companion
            if isSpecial:
                msg = "[🌟] " + companion
        else:
            msg = 'No companion yet. Get one at `+store`!'

        embed.add_field(name="Companion", value=msg, inline=False)

        #Acknowledgements
        ack = ''
        if self.meta.isAdmin(member):
            ack = ack + 'Server Administrator\n'
        elif self.meta.isMod(member):
            ack = ack + 'Server Moderator\n'
        elif self.meta.isStaff(member):
            ack = ack + 'Server Staff\n'

        if 'Certifying Team' in [role.name for role in member.roles]:
            ack = ack + 'Certifying Team Member\n'

        if 'Certified in Active Listening' in [role.name for role in member.roles]:
            ack = ack + 'Certified in Active Listening\n'

        if 'Listeners' in [role.name for role in member.roles]:
            ack = ack + 'Listener\n'

        if (ack != ''):
            embed.add_field(name="Acknowledgements", value=ack, inline=False)

        embed.set_thumbnail(url = pic)
        await ctx.send(embed=embed)

    @commands.command(alias=['propose'])
    async def marry(self, ctx, member: discord.Member = None):
        if member is None:
            embed = discord.Embed(
                description = 'Correct Usage: `+marry @user`.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

        id = ctx.author.id
        user = self.dbConnection.findProfile({"id": id})
        if user is None:
            embed = discord.Embed(
                title = 'Sorry, you don\'t have a profile yet! You can make one by using +profile.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return
        memberProfile = self.dbConnection.findProfile({"id": member.id})
        if memberProfile is None:
            embed = discord.Embed(
                title = 'Sorry, they don\'t have a profile yet! They can make one by using +profile.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

        if user['spouse'] != 0 or memberProfile['spouse'] != 0:
            embed = discord.Embed(
                title = 'One of you is already married!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

        if member == ctx.author:
            embed = discord.Embed(
                title = 'You can\'t marry yourself!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

        embed = discord.Embed(
            title = ctx.author.name + ' proposed to ' + member.name + '!',
            description = 'React to this message with a ❤ for yes, 💔 for no.\nYou have 60 seconds to decide!',
            color = discord.Color.teal()
        )
        await ctx.send(embed = embed)

        msg = ctx.channel.last_message
        await msg.add_reaction('❤')
        await msg.add_reaction('💔')

        emoji = ''

        def check(reaction, user):
            nonlocal emoji
            emoji = str(reaction.emoji)
            return user == member and (str(reaction.emoji) == '❤' or str(reaction.emoji) == '💔')

        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await channel.send('Timed out.')
        else:
            if emoji == '💔':
                embed = discord.Embed(
                    title = 'Yikes',
                    description = '<@' + str(member.id) + '> said no!',
                    color = discord.Color.teal()
                )
                await ctx.send(embed = embed)
                return

            self.dbConnection.updateProfile({"id": ctx.author.id}, {"$set": {"spouse": member.id}})
            self.dbConnection.updateProfile({"id": member.id}, {"$set": {"spouse": ctx.author.id}})

            choices = ['https://i.gifer.com/S3lf.gif',
                'https://66.media.tumblr.com/ed485a688fc03e4e8f5cdb3f4d01678b/tumblr_oyfmbl9N5W1rl58vno1_500.gif',
                'https://data.whicdn.com/images/330205015/original.gif',
                'https://66.media.tumblr.com/b46302ea92abcc8b1af97dd51f9cc434/tumblr_otrlkinIp61rdvr0eo1_500.gif',
                'https://media1.giphy.com/media/rnJuusfoWyu0U/giphy.gif',
                'https://www.alamedageek.com.br/wp-content/uploads/2017/01/upaltasaventuras.gif']

            embed = discord.Embed(
                title = 'Congratulations to the Newlyweds!',
                description = ctx.author.name + ' and ' + member.name + ' are now married!',
                color = discord.Color.teal()
            )
            embed.set_image(url = random.choice(choices))
            await ctx.send(embed = embed)

    @commands.command()
    async def divorce(self, ctx):
        id = ctx.message.author.id
        user = self.dbConnection.findProfile({"id": id})

        if user is None:
            embed = discord.Embed(
                title = 'Sorry, you don\'t have a profile yet! You can make one by using +profile.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

        spouse = user['spouse']

        if spouse == 0:
            embed = discord.Embed(
                title = 'You don\'t have a spouse to divorce.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

        embed = discord.Embed(
            title = 'Divorce ' + self.client.get_user(spouse).name + '?',
            description = 'React to this message with a ✅ for yes, ⛔ for no.\nYou have 60 seconds to decide!',
            color = discord.Color.teal()
        )
        await ctx.send(embed = embed)

        msg = ctx.channel.last_message
        await msg.add_reaction('✅')
        await msg.add_reaction('⛔')

        emoji = ''

        def check(reaction, user):
            nonlocal emoji
            emoji = str(reaction.emoji)
            return user == ctx.author and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '⛔')

        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await channel.send('Timed out.')
        else:
            if emoji == '⛔':
                embed = discord.Embed(
                    title = 'Divorce canceled.',
                    color = discord.Color.teal()
                )
                await ctx.send(embed = embed)
                return

            self.dbConnection.updateProfile({"id": ctx.author.id}, {"$set": {"spouse": 0}})
            self.dbConnection.updateProfile({"id": spouse}, {"$set": {"spouse": 0}})

            embed = discord.Embed(
                title = 'Divorced ' + self.client.get_user(spouse).name + '.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        id = member.id
        self.dbConnection.removeProfile({"id": id})

def setup(client):
    database_connection = Database()
    meta_class = Meta()
    client.add_cog(Profile(client, database_connection, meta_class))
