import discord
from discord.ext import commands
from database import Database
from .meta import Meta
#import meta

class Profile(commands.Cog):

    def __init__(self, client, database, meta):
        self.client = client
        self.dbConnection = database
        self.meta = meta

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

    @commands.command(aliases=[])
    async def giveSquad(self, ctx, squad, amt):
        if not self.meta.isAdmin(member):
            return

        squadDocs = self.dbConnection.findProfiles({'squad' : squad})

        for doc in squadDocs:
            self.dbConnection.updateProfile({'id': doc['id']}, {"$set": {"coins": (doc['coins']+amt)}})

        embed = discord.Embed(
            title = 'Consider it done! ✅',
            color = discord.Color.teal()
        )
        await ctx.send(embed = embed)

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
        elif teaHelped < coffeeHelped:
            coffeeName = coffeeName + '🙌🏻'
        if teaHelped > coffeeHelped:
            teaName = teaName + '🏅'
        elif teaHelped < coffeeHelped:
            coffeeName = coffeeName + '🏅'


        embed.add_field(name=teaName,value=teaStr)
        embed.add_field(name=coffeeName,value=coffeeStr, inline=False)

        await ctx.send(embed = embed)
        return

    @commands.command()
    async def squad(self, ctx, *, squad):
        if squad is None:
            embed = discord.Embed(
                description = 'Correct Usage: `+squad coffee/tea`',
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
            switcher = {
                #helped
                'Mouse':'https://www.wallpaperup.com/uploads/wallpapers/2013/10/20/163356/f2ee734991560fc269819a78f891e146-700.jpg',
                'Cat':'https://www.catster.com/wp-content/uploads/2018/03/Calico-cat-curled-up-asleep.jpg',
                'Goat':'https://www.smallholderfeed.co.uk/wp-content/uploads/2017/09/Goat-Feeding-Guide.jpg',
                'Parakeet':'https://i.ytimg.com/vi/yoYnevMnFlA/maxresdefault.jpg',
                'Snake':'https://resize.hswstatic.com/w_907/gif/coral-snake.jpg',
                'Hedgehog':'https://images2.minutemediacdn.com/image/upload/c_crop,h_2014,w_3584,x_0,y_187/f_auto,q_auto,w_1100/v1554918066/shape/mentalfloss/56004-istock-496545234.jpg',
                'Donkey':'https://images.fineartamerica.com/images/artworkimages/mediumlarge/1/12-miniature-donkey-foal-jean-louis-klein--marie-luce-hubert.jpg',
                'Wallaby':'https://www.australiangeographic.com.au/wp-content/uploads/2018/12/2T8A2202.jpg',
                'Fox':'https://i.redd.it/9vy19m3z2g421.png',
                'Corgi':'https://i.etsystatic.com/9905287/r/il/030f27/1483225420/il_794xN.1483225420_kjim.jpg',
                'Rock':'https://vignette.wikia.nocookie.net/spongebob/images/4/45/Pete_the_rock.png/revision/latest?cb=20141115223905',
                'Otter' : 'https://i.redd.it/iu459icfvv401.jpg',
                'Pig':'https://i.pinimg.com/originals/ee/2b/61/ee2b616224bfb8266217644f9ade0f22.jpg',
                'Shiba Inu':'https://66.media.tumblr.com/6075188a7f8b0fae3a9a137cd3cba5c3/tumblr_oispg8pBM31u0xpoxo1_1280.jpg',
                #coin
                'Baymax':'https://media0.giphy.com/media/Ak7083xqUqvXa/giphy.gif',
                'Niffler':'https://media.tenor.com/images/59452b5c5368f87cf36316403ad191b6/tenor.gif',
                'Husky':'https://i.chzbgr.com/original/8414926080/h5051269A/',
                'Toothless':'https://media1.giphy.com/media/1pA8TwX8atOCnAtTbV/giphy.gif',
                'Yamper' : 'https://thumbs.gfycat.com/SecondhandLawfulGalapagoshawk-size_restricted.gif',
                'Puffin':'https://www.audubon.org/sites/default/files/styles/hero_cover_bird_page/public/web_h_a1_5428_5_atlantic-puffin_lorraine_minns-breeding-adult.jpg?itok=XYcRrHhm',
                'Charmander':'https://media.giphy.com/media/erHPszvivFn44/giphy.gif',
                'Bulbasaur':'https://media0.giphy.com/media/MMK9pcpsSa9gI/giphy.gif',
                'Squirtle':'https://media.giphy.com/media/8gPs3nAIqtzvW/giphy.gif',
                'Oshawott':'https://media2.giphy.com/media/rk391iLXWhQIg/source.gif',
                'Mudkip':'https://thumbs.gfycat.com/FrigidShyJaguar-size_restricted.gif',
                'Psyduck':'http://31.media.tumblr.com/tumblr_m1igknqbmB1qc2jhfo6_250.gif',
                'Pikachu':'http://49.media.tumblr.com/540ad0eb71628f0768adce2876962e50/tumblr_o2tesgL5vt1sr6y44o2_500.gif',
                'Shaymin':'http://45.media.tumblr.com/c3c6b13035a5392183a6676673ecab0c/tumblr_np1gr1IlFv1tdtetdo1_500.gif',
                'Eevee':'https://media1.tenor.com/images/1df3441f8f9639e4661475009177b42f/tenor.gif?itemid=12016437',
                'Vaporeon':'https://media1.giphy.com/media/sJ29qAcpPO9uo/source.gif',
                'Jolteon':'https://media3.giphy.com/media/et6sLQpNiedB6/giphy.gif',
                'Espeon':'https://data.whicdn.com/images/254804480/original.gif',
                'Flareon':'https://data.whicdn.com/images/85904853/original.gif',
                'Umbreon':'https://66.media.tumblr.com/65feeda7b4cd6111353e493fc11303bb/tumblr_inline_p7obtc4AoJ1sbpdql_500.gif',
                'Leafeon':'https://data.whicdn.com/images/332118464/original.gif',
                'Sylveon':'https://steamuserimages-a.akamaihd.net/ugc/964220763826312953/E630A4546A45E8E6B04642B91D5E7FEAED7D3318/',
                'Glaceon':'https://em.wattpad.com/c95e8e70e6b4ed82ba13e4ee344056c276dc4cae/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f776174747061642d6d656469612d736572766963652f53746f7279496d6167652f4148704e334264336d324d314b673d3d2d3434363639323536342e313464353763613531373630653532313836323836313638333637372e676966?s=fit&w=720&h=720',
            }
            embed.set_image(url = switcher.get(companion, "none"))

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
