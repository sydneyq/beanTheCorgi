import discord
from discord.ext import commands
from database import Database
from .meta import Meta

class Currency(commands.Cog):

    def __init__(self, client, database, meta):
        self.client = client
        self.dbConnection = database
        self.meta = meta

    @commands.command(aliases=['shop', 'companions', 'pets'])
    async def store(self, ctx):
        id = ctx.author.id
        user = self.dbConnection.findProfile({"id": id})
        helped = user['helped']
        coins = user['coins']

        embed = discord.Embed(
            title = 'Store',
            description = 'You have:\t`' + str(helped) + '` Helped\t`' + str(coins) + '` Coins',
            color = discord.Color.teal()
        )

        storeHelp = """Helped Companions are companions you unlock with your Helped People count.
                        Coin Companions are companions you can buy through coins. They're gifs!
                        `+buy companionName` for Coin Companions, `+set companionName` for Helped Companions."""
        embed.add_field(name='Store Help', value=storeHelp, inline=False)

        helpedCompanions = """1 Helped : \tMouse
                                10 Helped : \tCat
                                10 Helped : \tGoat
                                20 Helped : \tParakeet
                                20 Helped : \tSnake
                                40 Helped : \tMiniature Donkey
                                40 Helped : \tWallaby
                                70 Helped : \tFox
                                70 Helped : \tHedgehog
                                100 Helped : \tBean the Corgi
                            """
        embed.add_field(name='Helped Companions', value=helpedCompanions)

        coinCompanions = """100 coins : \tBaymax
                            100 coins : \tPet Rock
                            100 coins : \tPig
                            300 coins : \tNiffler
                            300 coins : \tHusky Puppy
                            300 coins : \tPuffin
                            500 coins : \tToothless
                            500 coins : \tShiba Inu
                            """
        embed.add_field(name='Coin Companions', value=coinCompanions)

        embed.set_footer(text = """You can only have one companion, and will have to rebuy any Coin Companions you change from.""")
        await ctx.send(embed = embed)

        #coins
    @commands.command()
    async def buy(self, ctx, *, companion):
        id = ctx.author.id
        user = self.dbConnection.findProfile({"id": id})
        coins = user['coins']
        switcher = {
            'Baymax':100,
            'Pet Rock':100,
            'Pig':100,
            'Niffler':300,
            'Husky Puppy':300,
            'Puffin':300,
            'Toothless':500,
            'Shiba Inu':500,
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

    @commands.command(aliases=['removeCompanion', 'release'])
    async def resetCompanion(self, ctx):
        id = ctx.author.id
        user = self.dbConnection.findProfile({"id": id})
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
        helped = user['helped']

        switcher = {
            'Mouse': 1,
            'Cat': 10,
            'Goat': 10,
            'Parakeet': 20,
            'Snake': 20,
            'Miniature Donkey': 40,
            'Wallaby':40,
            'Hedgehog': 70,
            'Fox':70,
            'Bean the Corgi':100
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
    async def give(self, ctx, member: discord.Member, amt):
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

    @commands.command()
    async def take(self, ctx, member: discord.Member, amt):
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
            helped = user['helped']
            helped = helped + 1
            self.dbConnection.updateProfile({"id": id}, {"$set": {"helped": helped}})
            embed = discord.Embed(
                title = 'Repped ' + member.name + '!',
                description = member.name + '\'s rep count: ' + str(helped),
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)


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
            helped = user['helped']
            helped = helped - 1
            self.dbConnection.updateProfile({"id": id}, {"$set": {"helped": helped}})
            embed = discord.Embed(
                title = 'Derepped ' + member.name + '!',
                description = member.name + '\'s rep count: ' + str(helped),
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

def setup(client):
    database_connection = Database()
    meta_class = Meta()
    client.add_cog(Currency(client, database_connection, meta_class))
