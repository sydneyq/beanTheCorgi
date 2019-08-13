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

    async def get_profile(member: discord.Member = None):
        if member is None:
            return

        id = member.id

        profile = self.dbConnection.findProfile({"id": id})
        if profile is None:
            self.dbConnection.insertProfile({'id': id, 'squad': '', 'helped': 0, 'coins': 0, 'companion': '', 'spouse': 0})
            profile = self.dbConnection.findProfile({"id": id})

        return profile

    @commands.command()
    async def squad(self, ctx, *, squad):
        squad = squad.lower()
        # see whats in the message -> adjust the specific persons profile based  on it
        # .update "updates" the profile $ must be used to keep old items
        id = ctx.author.id
        #user = self.dbConnection.findProfile({"id": id})
        user = self.dbConnection.findProfile({"id": id})
        print('Finding profile...')
        if user is None:
            self.dbConnection.insertProfile({'id': id, 'squad': '', 'helped': 0, 'coins': 0, 'companion': '', 'spouse': 0})
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
            self.dbConnection.insertProfile({'id': id, 'squad': '', 'helped': 0, 'coins': 0, 'companion': '', 'spouse': 0})
            user = self.dbConnection.findProfile({"id": id})

        pic = member.avatar_url

        #Basics
        if (user['squad'] == "Tea"):
            embed = discord.Embed(color=0xa72461)
            embed.add_field(name="Squad", value=user['squad'], inline=False)
            embed.set_author(name = name, icon_url = 'https://cdn2.stylecraze.com/wp-content/uploads/2015/04/2072_11-Surprising-Benefits-And-Uses-Of-Marijuana-Tea_shutterstock_231770824.jpg')
        elif (user['squad'] == "Coffee"):
            embed = discord.Embed(color=0xff5858)
            embed.add_field(name="Squad", value=user['squad'], inline=False)
            embed.set_author(name = name, icon_url = 'https://www.caffesociety.co.uk/assets/recipe-images/latte-small.jpg')
        else:
            embed = discord.Embed(
                color = discord.Color.teal()
            )
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
            msg = 'No companion'
        embed.add_field(name="Companion", value=msg, inline=True)

        if companion is not '':
            switcher = {
                'Mouse':'https://www.wallpaperup.com/uploads/wallpapers/2013/10/20/163356/f2ee734991560fc269819a78f891e146-700.jpg',
                'Cat':'https://www.catster.com/wp-content/uploads/2018/03/Calico-cat-curled-up-asleep.jpg',
                'Goat':'https://www.smallholderfeed.co.uk/wp-content/uploads/2017/09/Goat-Feeding-Guide.jpg',
                'Parakeet':'https://i.ytimg.com/vi/yoYnevMnFlA/maxresdefault.jpg',
                'Snake':'https://resize.hswstatic.com/w_907/gif/coral-snake.jpg',
                'Hedgehog':'https://images2.minutemediacdn.com/image/upload/c_crop,h_2014,w_3584,x_0,y_187/f_auto,q_auto,w_1100/v1554918066/shape/mentalfloss/56004-istock-496545234.jpg',
                'Miniature Donkey':'https://images.fineartamerica.com/images/artworkimages/mediumlarge/1/12-miniature-donkey-foal-jean-louis-klein--marie-luce-hubert.jpg',
                'Wallaby':'https://www.australiangeographic.com.au/wp-content/uploads/2018/12/2T8A2202.jpg',
                'Fox':'https://i.redd.it/9vy19m3z2g421.png',
                'Bean the Corgi':'https://i.etsystatic.com/9905287/r/il/030f27/1483225420/il_794xN.1483225420_kjim.jpg',
                'Baymax':'https://media0.giphy.com/media/Ak7083xqUqvXa/giphy.gif',
                'Pet Rock':'https://vignette.wikia.nocookie.net/spongebob/images/4/45/Pete_the_rock.png/revision/latest?cb=20141115223905',
                'Pig':'https://media1.giphy.com/media/3o6EhCzemk7soHRLnG/source.gif',
                'Niffler':'https://media.tenor.com/images/59452b5c5368f87cf36316403ad191b6/tenor.gif',
                'Husky Puppy':'https://i.chzbgr.com/original/8414926080/h5051269A/',
                'Puffin':'https://media0.giphy.com/media/XptC1OfIlLy6SUuyXh/giphy.gif',
                'Toothless':'https://media1.giphy.com/media/1pA8TwX8atOCnAtTbV/giphy.gif',
                'Shiba Inu':'https://media2.giphy.com/media/D6InoH7TLxMsM/giphy.gif'
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
