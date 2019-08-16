import discord
from discord.ext import commands
from database import Database
from .meta import Meta
import json
import os

class Profile(commands.Cog):

    def __init__(self, client, database, meta):
        self.client = client
        self.dbConnection = database
        self.meta = meta

        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'docs/store.json')

        with open(filename) as json_file:
            self.store = json.load(json_file)
    '''
    async def get_profile(member: discord.Member = None):
        if member is None:
            return

        id = member.id

        profile = self.dbConnection.findProfile({"id": id})
        if profile is None:
            self.dbConnection.insertProfile({'id': id, 'squad': '', 'helped': 0, 'coins': 50, 'companion': '', 'spouse': 0})
            profile = self.dbConnection.findProfile({"id": id})

        return profile
    '''

    @commands.command(aliases=['squads', 'squadcount', 's', 'sq', 'leaderboard'])
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
            print('No squad found. Assigning...')
            if 'tea' in squad:
                self.dbConnection.updateProfile({"id": id}, {"$set": {"squad": "Tea"}})
                embed = discord.Embed(
                    title = 'You\'ve joined the Tea Squad!',
                    color = discord.Color.teal()
                )
                await ctx.send(embed = embed)
                return
            elif 'coffee' in squad:
                self.dbConnection.updateProfile({"id": id}, {"$set": {"squad": "Coffee"}})
                embed = discord.Embed(
                    title = 'You\'ve joined the Coffee Squad!',
                    color = discord.Color.teal()
                )
                await ctx.send(embed = embed)
                return
            else:
                embed = discord.Embed(
                    title = 'That Squad doesn\'t exist. Please choose either Coffee or Tea.',
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
            embed.add_field(name="Squad", value=user['squad'], inline=False)
            embed.set_author(name = name, icon_url = 'https://cdn2.stylecraze.com/wp-content/uploads/2015/04/2072_11-Surprising-Benefits-And-Uses-Of-Marijuana-Tea_shutterstock_231770824.jpg')
        elif (user['squad'] == "Coffee"):
            embed = discord.Embed(color=0x9cf196)
            embed.add_field(name="Squad", value=user['squad'], inline=False)
            embed.set_author(name = name, icon_url = 'https://www.caffesociety.co.uk/assets/recipe-images/latte-small.jpg')
        else:
            embed = discord.Embed(color = discord.Color.teal())
            embed.add_field(name="Squad", value='No Squad yet. Use `+squad tea/coffee` to join one!', inline=False)
            embed.set_author(name = name)

        embed.set_footer(text = 'Mind Café', icon_url = 'https://media.discordapp.net/attachments/591611902459641856/593267453363224588/Bean_Icon.png')

        #Achievements
        #   helped
        helped = user['helped']
        embed.add_field(name="People Helped", value=helped, inline=True)

        #   coins
        coins = user['coins']
        embed.add_field(name="Coins", value=coins, inline=True)

        #   companion
        companion = user['companion']
        msg = companion
        if msg == '':
            msg = 'No companion yet. Get one at `+store`!'
        embed.add_field(name="Companion", value=msg, inline=True)

        if companion is not '':
            isCoin = False
            for c in self.store['Coin Companions']:
                if c['name'].lower() == companion.lower():
                    embed.set_image(url = c['src'])
                    isCoin = True
                    break

            if not isCoin:
                for c in self.store['Helped Companions']:
                    if c['name'].lower() == companion.lower():
                        embed.set_image(url = c['src'])
                        break


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

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        self.dbConnection.removeProfile({"id": id})

def setup(client):
    database_connection = Database()
    meta_class = Meta()
    client.add_cog(Profile(client, database_connection, meta_class))
