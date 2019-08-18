import discord
from discord.ext import commands
from database import Database
from .meta import Meta
import random
import json
import os
import asyncio

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
            embed.add_field(name='Store Commands', value=storeDesc, inline=False)

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
            embed.set_footer(text = 'Earn coins by participating in server events! Read #about-profiles for more information. Access this store using "+store c".')
            await ctx.send(embed = embed)
            return
        #helped
        elif type.lower() == 'helped' or type.lower() == 'h':
            storeHelp = """You can unlock these Companions with Help Points. After reaching the minimum amount Helped, you're able to keep these Companions!"""
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
            embed.set_footer(text = 'Earn Help Points by supporting others! Read #about-profiles for more information. Access this store using "+store h".')
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
            embed.set_footer(text = 'Earn coins by participating in server events! Read #about-profiles for more information. Access this store using "+store i".')
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

    @commands.command(aliases=['set', 'purchase'])
    async def buy(self, ctx, *, input):
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
        helped = user['helped']
        c = 0

        for c in self.store['Coin Companions']:
            if c['name'].lower() == input.lower():
                if coins >= c['price']:
                    coins -= c['price']
                    self.dbConnection.updateProfile({"id": id}, {"$set": {"coins": coins, "companion": c['name']}})
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

        for c in self.store['Helped Companions']:
            if c['name'].lower() == input.lower():
                if helped >= c['price']:
                    self.dbConnection.updateProfile({"id": id}, {"$set": {"companion": c['name']}})
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

        for i in self.store['Items']:
            if i['name'].lower() == input.lower():
                if coins >= i['price']:
                    coins -= i['price']

                    if i['name'].lower() == 'squad swap':
                        if user['squad'] == 'Coffee':
                            self.dbConnection.updateProfile({"id": id}, {"$set": {"coins": coins, "squad": 'Tea'}})
                            role = ctx.guild.get_role(612788003542401035)
                            await ctx.author.add_roles(role)
                        else:
                            self.dbConnection.updateProfile({"id": id}, {"$set": {"coins": coins, "squad": 'Coffee'}})
                            role = ctx.guild.get_role(612788004926521365)
                            await ctx.author.add_roles(role)

                    embed = discord.Embed(
                        title = 'Consider it done! ✅',
                        color = discord.Color.teal()
                    )
                    await ctx.send(embed = embed)
                else:
                    embed = discord.Embed(
                        title = 'You can\'t seem to afford that item.',
                        color = discord.Color.teal()
                    )
                    await ctx.send(embed = embed)
                return


        embed = discord.Embed(
            title = 'I couldn\'t seem to find companion or item.',
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
    async def releaseCompanion(self, ctx):
        id = ctx.author.id
        user = self.dbConnection.findProfile({"id": id})

        if user is None:
            embed = discord.Embed(
                title = 'Sorry, you don\'t have a profile yet! You can make one by using +profile.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

        embed = discord.Embed(
            title = 'Release your Companion?',
            description = 'React to this message with a ✅ for yes, ⛔ for no.\nYou have 60 seconds to decide!',
            color = discord.Color.teal()
        )
        await ctx.send(embed = embed)

        msgs = []
        async for msg in ctx.channel.history(limit=1):
            if (msg.author.id == 592436047175221259 or msg.author.id == 432038389663924225):
                msgs.append(msg)
                break

        msg = msgs[0]
        await msg.add_reaction('✅')
        await msg.add_reaction('⛔')

        emoji = ''

        def check(reaction, user):
            #print('str: ' + str(reaction.emoji))
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
                    title = 'Release canceled.',
                    color = discord.Color.teal()
                )
                await ctx.send(embed = embed)
                return
            print('emoji: ' + emoji)

            self.dbConnection.updateProfile({"id": id}, {"$set": {"companion": ''}})

            embed = discord.Embed(
                title = 'You released your companion!',
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

        userDiscord = discord.utils.get(self.client.get_all_members(), id=id)

        embed = discord.Embed(
            title = 'You\'ve been given `' + str(amt) + '` coins!',
            description = 'Your total: `' + str(coins) + '` coins',
            color = discord.Color.teal()
        )
        if reason != '':
            embed.add_field(name='Reason: ', value=reason)
        embed.set_thumbnail(url = 'https://www.mariowiki.com/images/thumb/1/17/CoinMK8.png/1200px-CoinMK8.png')

        try:
            await userDiscord.send(embed = embed)
        except:
            print('Could not send private message.')

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

        msg = '**<@' + str(member.id) + '>** was given ' + str(amt) + ' coins by **' + ctx.author.name + '**.'
        if (reason != ''):
            msg += '\n```' + reason + '```'

        await log.send(msg)


    @commands.command()
    async def giveSquad(self, ctx, squad, amt: int, reason = ''):
        if not self.meta.isAdmin(ctx.author):
            return

        squad = squad.lower()
        squad = squad.capitalize()
        squadDocs = self.dbConnection.findProfiles({'squad' : squad})

        for doc in squadDocs:
            self.dbConnection.updateProfile({'id': doc['id']}, {"$set": {"coins": (doc['coins']+amt)}})

        embed = discord.Embed(
            title = 'Consider it done! ✅',
            color = discord.Color.teal()
        )
        await ctx.send(embed = embed)

        #finding log channel
        guild = ctx.guild
        for ch in guild.text_channels:
            if ch.name.lower() == 'log':
                log = guild.get_channel(ch.id)
                break

        msg = 'The **' + squad + ' Squad** was given ' + str(amt) + ' coins by **' + ctx.author.name + '**.'
        if (reason != ''):
            msg += '\n```' + reason + '```'

        await log.send(msg)

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

        msg = '**<@' + str(member.id) + '>** lost ' + str(amt) + ' coins by **' + ctx.author.name + '**.'
        if (reason != ''):
            msg += '\n```' + reason + '```'

        await log.send(msg)

    @commands.command(aliases=['rep', 'thanks'])
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
