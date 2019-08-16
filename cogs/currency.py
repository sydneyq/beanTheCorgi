import discord
from discord.ext import commands
from database import Database
from .meta import Meta
import random
import json
import os

class Currency(commands.Cog):

    def __init__(self, client, database, meta):
        self.client = client
        self.dbConnection = database
        self.meta = meta

        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'docs/store.json')

        with open(filename) as json_file:
            self.store = json.load(json_file)

    @commands.command(aliases=['shop', 'companions', 'pets', '$', 'sh', 'st'])
    async def store(self, ctx, type: str = None):
        id = ctx.author.id
        user = self.dbConnection.findProfile({"id": id})

        if user is None:
            embed = discord.Embed(
                title = 'Sorry, you don\'t have a profile yet! You can make one by using +profile.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

        helped = user['helped']
        coins = user['coins']

        embed = discord.Embed(
            title = 'Store',
            description = 'You have:\t`' + str(helped) + '` Helped\t`' + str(coins) + '` Coins',
            color = discord.Color.teal()
        )

        #default store
        if type is None:
            storeHelp = """Welcome to the Store! This is where you can reap the rewards of your hard work."""
            embed.add_field(name='Store Help', value=storeHelp, inline=False)

            storeDesc = """`+store c` - Coin Companion Store
            `+store h` - Helped Companion Store
            `+store i` - Item Store"""
            embed.add_field(name='Coin Companions', value=storeDesc, inline=False)

            embed.set_thumbnail(url = 'https://cdn.discordapp.com/emojis/602910572153143337.png?v=1')
            embed.set_footer(text = 'Need help with profiles or currency? Check #about-profiles!')
            await ctx.send(embed = embed)
            return
        #coin
        elif type.lower() == 'coin' or type.lower() == 'c' or type.lower() == 'coins':
            storeHelp = """You can buy these Companions with Coins. They're gifs! You do not keep a Coin Companion if you set or buy a different Companion."""
            embed.add_field(name='Store Help', value=storeHelp, inline=False)
            storeDesc = ''
            prevCost = 0

            for item in self.store['Coin Companions']:
                #same price, add to same line
                if item['price'] == prevCost:
                    storeDesc += ', ' + item['name']
                #different price, new line, update prevCost
                else:
                    storeDesc += '\n`' + str(item['price']) + ' coins:` ' + item['name']
                    prevCost = item['price']

            embed.add_field(name='Coin Companions', value=storeDesc, inline=False)
            embed.set_thumbnail(url = 'https://www.mariowiki.com/images/thumb/1/17/CoinMK8.png/1200px-CoinMK8.png')
            embed.set_footer(text = 'Earn coins by participating in server events! Read #about-profiles for more information. Access this store using "+store c."')
            await ctx.send(embed = embed)
            return
        #helped
        elif type.lower() == 'helped' or type.lower() == 'h':
            storeHelp = """You can unlock these Companions with Help Points. After reaching the minimum amount Helped, you're able to keep these Companions!."""
            embed.add_field(name='Store Help', value=storeHelp, inline=False)
            storeDesc = ''
            prevCost = 0

            for item in self.store['Helped Companions']:
                #same price, add to same line
                if item['price'] == prevCost:
                    storeDesc += ', ' + item['name']
                #different price, new line, update prevCost
                else:
                    storeDesc += '\n`' + str(item['price']) + ' helped:` ' + item['name']
                    prevCost = item['price']

            embed.add_field(name='Helped Companions', value=storeDesc, inline=False)
            embed.set_thumbnail(url = 'https://img.pngio.com/mario-bros-star-png-png-image-mario-bros-star-png-240_215.png')
            embed.set_footer(text = 'Earn Help Points by supporting others! Read #about-profiles for more information. Access this store using "+store h."')
            await ctx.send(embed = embed)
            return
        #item
        elif type.lower() == 'item' or type.lower() == 'i' or type.lower() == 'items':
            storeHelp = """You can buy these items with Coins. Items will immediately be used upon purchase."""
            embed.add_field(name='Store Help', value=storeHelp, inline=False)
            storeDesc = ''
            prevCost = 0

            for item in self.store['Items']:
                #same price, add to same line
                if item['price'] == prevCost:
                    storeDesc += ', ' + item['name']
                #different price, new line, update prevCost
                else:
                    storeDesc += '\n`' + str(item['price']) + ' coins:` ' + item['name']
                    prevCost = item['price']

            embed.add_field(name='Items', value=storeDesc, inline=False)
            embed.set_thumbnail(url = 'https://vignette.wikia.nocookie.net/mariokart/images/a/aa/Golden_Mushroom_-_Mario_Kart_Wii.png/revision/latest?cb=20180115185605')
            embed.set_footer(text = 'Earn coins by participating in server events! Read #about-profiles for more information. Access this store using "+store i."')
            await ctx.send(embed = embed)
            return
        #unknown type
        else:
            embed2 = discord.Embed(
                description = 'Correct Usage: \n`+store` \n`store [coin/helped/item]`',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed2)
            return

        storeHelp = """Helped Companions are companions you unlock with your Helped People count.
                        Coin Companions are companions you can buy through coins. They're gifs!
                        `+buy companionName` for Coin Companions, `+set companionName` for Helped Companions."""
        embed.add_field(name='Store Help', value=storeHelp, inline=False)

        '''
        helpedCompanions = """`1 Helped` \tMouse
        `1 Helped` \tRock
        `5 Helped` \tCat
        `10 Helped` \tGoat
        `10 Helped` \tParakeet
        `10 Helped` \tRaccoon
        `20 Helped` \tSnake
        `20 Helped` \tWallaby
        `30 Helped` \tDonkey
        `30 Helped` \tPig
        `30 Helped` \tPuffin
        `40 Helped` \tFox
        `40 Helped` \tHedgehog
        `40 Helped` \tOtter
        `50 Helped` \tShiba Inu
        `50 Helped` \tCorgi
        """
        '''


        embed.add_field(name='Helped Companions', value=helpedCompanions, inline=True)

        coinCompanions = """`50 coins` \tBulbasaur
        `50 coins` \tCharmander
        `50 coins` \tSquirtle
        `100 coins` \tBaymax
        `100 coins` \tOshawott
        `100 coins` \tPsyduck
        `300 coins` \tNiffler
        `300 coins` \tHusky
        `300 coins` \tShaymin
        `500 coins` \tToothless
        `500 coins` \tPikachu
        `500 coins` \tMudkip
        `700 coins` \tYamper
        `700 coins` \tEevee
        """
        embed.add_field(name='Coin Companions', value=coinCompanions, inline=True)

        embed.set_footer(text = """You can only have one companion, and will have to rebuy any Coin Companions you change from.""")
        await ctx.send(embed = embed)

        #coins
    @commands.command()
    async def buy(self, ctx, *, companion):
        id = ctx.author.id
        user = self.dbConnection.findProfile({"id": id})

        if user is None:
            embed = discord.Embed(
                title = 'Sorry, you don\'t have a profile yet! You can make one by using +profile.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

        coins = user['coins']
        switcher = {
            'Bulbasaur':50,
            'Charmander':50,
            'Squirtle':50,
            'Baymax':100,
            'Oshawott':100,
            'Psyduck':100,
            'Niffler':300,
            'Husky':300,
            'Shaymin':300,
            'Toothless':500,
            'Pikachu':500,
            'Mudkip':500,
            'Yamper':700,
            'Eevee':700
        }

        cost = switcher.get(companion, 'none')
        if cost is 'none':
            embed = discord.Embed(
                title = 'I couldn\'t seem to find that companion.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

        if coins >= cost:
            coins -= cost
            self.dbConnection.updateProfile({"id": id}, {"$set": {"coins": coins, "companion": companion}})
            embed = discord.Embed(
                title = 'Consider it done! ✅',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                title = 'You can\'t seem to afford that companion.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

    @commands.command(aliases=['evolveCompanion'])
    async def evolve(self, ctx):
        id = ctx.author.id
        user = self.dbConnection.findProfile({"id": id})

        if user is None:
            embed = discord.Embed(
                title = 'Sorry, you don\'t have a profile yet! You can make one by using +profile.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

        if user['companion'] != 'Eevee':
            print('Companion: ' + user['companion'])
            embed = discord.Embed(
                title = 'You need an Eevee to evolve!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return
        else:
            choices = ['Flareon',
                'Jolteon',
                'Glaceon',
                'Umbreon',
                'Leafeon',
                'Espeon',
                'Vaporeon',
                'Sylveon']

            result = random.choice(choices)

            self.dbConnection.updateProfile({"id": id}, {"$set": {"companion": result}})

            embed = discord.Embed(
                title = 'Consider it done! ✅\nYour companion is now a ' + result + '!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

    @commands.command(aliases=['removeCompanion', 'release'])
    async def resetCompanion(self, ctx):
        id = ctx.author.id
        user = self.dbConnection.findProfile({"id": id})

        if user is None:
            embed = discord.Embed(
                title = 'Sorry, you don\'t have a profile yet! You can make one by using +profile.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

        self.dbConnection.updateProfile({"id": id}, {"$set": {"companion": ''}})
        embed = discord.Embed(
            title = 'You released your companion!',
            color = discord.Color.teal()
        )
        await ctx.send(embed = embed)

    @commands.command()
    async def set(self, ctx, *, companion):
        id = ctx.author.id
        user = self.dbConnection.findProfile({"id": id})

        if user is None:
            embed = discord.Embed(
                title = 'Sorry, you don\'t have a profile yet! You can make one by using +profile.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

        helped = user['helped']

        switcher = {
            'Mouse': 1,
            'Cat': 5,
            'Rock': 1,
            'Goat': 10,
            'Parakeet': 10,
            'Raccoon': 10,
            'Snake': 20,
            'Wallaby':20,
            'Donkey': 30,
            'Pig': 30,
            'Puffin': 30,
            'Hedgehog': 40,
            'Fox':40,
            'Otter':40,
            'Shiba Inu':50,
            'Corgi':50
        }

        cost = switcher.get(companion, 'none')
        if cost is 'none':
            embed = discord.Embed(
                title = 'I couldn\'t seem to find that companion.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

        if helped >= cost:
            self.dbConnection.updateProfile({"id": id}, {"$set": {"companion": companion}})
            embed = discord.Embed(
                title = 'Consider it done! ✅',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                title = 'You can\'t seem to afford that companion.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

    @commands.command()
    async def give(self, ctx, member: discord.Member, amt, *, reason = ''):
        if not self.meta.isAdmin(ctx.author):
            return

        id = member.id
        user = self.dbConnection.findProfile({"id": id})
        coins = user['coins']
        coins = coins + int(amt)
        self.dbConnection.updateProfile({"id": id}, {"$set": {"coins": coins}})
        embed = discord.Embed(
            title = 'Gave ' + member.name + ' ' + str(amt) + ' coins!',
            description = member.name + '\'s coin count: ' + str(coins),
            color = discord.Color.teal()
        )
        await ctx.send(embed = embed)

        #finding log channel
        guild = ctx.guild
        for ch in guild.text_channels:
            if ch.name.lower() == 'log':
                log = guild.get_channel(ch.id)
                break

        msg = '**<@' + str(member.id) + '>** was given ' + str(amt) + ' coins by <@' + str(ctx.author.id) + '>.'
        if (reason != ''):
            msg += '\n```' + reason + '```'

        await log.send(msg)

    @commands.command(aliases=['givesquad'])
    async def giveSquad(self, ctx, squad, amt: int):
        if not self.meta.isAdmin(ctx.author):
            return

        squadDocs = self.dbConnection.findProfiles({'squad' : squad})

        for doc in squadDocs:
            self.dbConnection.updateProfile({'id': doc['id']}, {"$set": {"coins": (doc['coins']+amt)}})

        embed = discord.Embed(
            title = 'Consider it done! ✅',
            color = discord.Color.teal()
        )
        await ctx.send(embed = embed)

    @commands.command()
    async def take(self, ctx, member: discord.Member, amt, *, reason = ''):
        if not self.meta.isAdmin(ctx.author):
            return

        id = member.id
        user = self.dbConnection.findProfile({"id": id})
        coins = user['coins']
        coins = coins - int(amt)
        self.dbConnection.updateProfile({"id": id}, {"$set": {"coins": coins}})
        embed = discord.Embed(
            title = 'Took ' + str(amt) + ' coins from ' + member.name + '!',
            description = member.name + '\'s coin count: ' + str(coins),
            color = discord.Color.teal()
        )
        await ctx.send(embed = embed)

        #finding log channel
        guild = ctx.guild
        for ch in guild.text_channels:
            if ch.name.lower() == 'log':
                log = guild.get_channel(ch.id)
                break

        msg = '**<@' + str(member.id) + '>** lost ' + str(amt) + ' coins by <@' + str(ctx.author.id) + '>.'
        if (reason != ''):
            msg += '\n```' + reason + '```'

        await log.send(msg)

    @commands.command(aliases=['rep', 'helpedby', 'thanks'])
    async def helpedBy(self, ctx, member: discord.Member = None):
        if member is None:
            embed = discord.Embed(
                title = 'Please tag a person you\'d like to rep!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return
        elif ctx.author.id == member.id:
            embed = discord.Embed(
                title = 'You can\'t rep yourself!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return
        else:
            id = member.id
            user = self.dbConnection.findProfile({"id": id})

            if user is None:
                embed = discord.Embed(
                    title = 'Sorry, they don\'t have a profile yet! They can make one by using +profile.',
                    color = discord.Color.teal()
                )
                await ctx.send(embed = embed)
                return

            helped = user['helped']
            helped = helped + 1
            self.dbConnection.updateProfile({"id": id}, {"$set": {"helped": helped}})
            embed = discord.Embed(
                title = 'Repped ' + member.name + '!',
                description = member.name + '\'s rep count: ' + str(helped),
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

        #finding log channel
        guild = ctx.guild
        for ch in guild.text_channels:
            if ch.name.lower() == 'log':
                log = guild.get_channel(ch.id)
                break

        msg = '**<@' + str(member.id) + '>** was repped by <@' + str(ctx.author.id) + '>.'

        await log.send(msg)


    @commands.command(aliases=['derep'])
    async def removeHelped(self, ctx, member: discord.Member = None):
        if not self.meta.isAdmin(ctx.author):
            return

        if member is None:
            embed = discord.Embed(
                title = 'Please tag a person you\'d like to derep!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return
        else:
            id = member.id
            user = self.dbConnection.findProfile({"id": id})

            if user is None:
                embed = discord.Embed(
                    title = 'Sorry, they don\'t have a profile yet! They can make one by using +profile.',
                    color = discord.Color.teal()
                )
                await ctx.send(embed = embed)
                return

            helped = user['helped']
            helped = helped - 1
            self.dbConnection.updateProfile({"id": id}, {"$set": {"helped": helped}})
            embed = discord.Embed(
                title = 'Derepped ' + member.name + '!',
                description = member.name + '\'s rep count: ' + str(helped),
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

        #finding log channel
        guild = ctx.guild
        for ch in guild.text_channels:
            if ch.name.lower() == 'log':
                log = guild.get_channel(ch.id)
                break

        msg = '**<@' + str(member.id) + '>** was derepped by <@' + str(ctx.author.id) + '>.'

        await log.send(msg)

def setup(client):
    database_connection = Database()
    meta_class = Meta()
    client.add_cog(Currency(client, database_connection, meta_class))
