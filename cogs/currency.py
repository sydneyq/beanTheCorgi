import discord
from discord.ext import commands
from database import Database
from .meta import Meta
import random
import json
import os
import asyncio
from numpy.random import choice
import secret

class Currency(commands.Cog):

    def __init__(self, client, database, meta):
        self.client = client
        self.dbConnection = database
        self.meta = meta

        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'docs/store.json')

        with open(filename) as json_file:
            self.store = json.load(json_file)


    @commands.cooldown(1, 60*60*24, commands.BucketType.user)
    @commands.command(aliases=['treasurehunt', 'treasure'])
    async def daily(self, ctx):
        id = ctx.message.author.id

        user = self.dbConnection.findProfile({"id": id})

        if user is None:
            embed = discord.Embed(
                title = 'Sorry, you don\'t have a profile yet! You can make one by using +profile.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

        companion = user['companion']
        if companion == '':
            embed = discord.Embed(
                title = 'Sorry, you need a companion for that!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

        special = False
        elements = [10, 25, 50]
        weights = [0.6, 0.3, 0.1]

        if companion in [item['name'] for item in self.store['Special Companions']]:
            special = True
            weights = [0.4, 0.35, 0.25]

        amt = choice(elements, p=weights)

        coins = user['coins']
        coins = coins + int(amt)
        self.dbConnection.updateProfile({"id": id}, {"$set": {"coins": coins}})

        print('making embed')
        embed = discord.Embed(
            title = ctx.author.name + ', your ' + companion + ' found `' + str(amt) + '` coins!',
            description = '<@' + str(id) + '> coin count: `' + str(coins) + '`',
            color = discord.Color.teal()
        )

        print('checking url')
        if companion != '':
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
                        break

        print('is special')
        if special:
            embed.set_footer(text = 'Special Companion detected! You have a higher chance of getting more coins.')
        print('sending embed')
        await ctx.channel.send(embed = embed)

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
            storeHelp = """You can buy these Companions with Coins and using `+buy companionName`. You do not keep a Coin Companion if you set or buy a different Companion. Special Companions are evolvable and have a higher chance for more daily coins."""
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

            storeDesc_special = ''
            for item in self.store['Special Companions']:
                #same price, add to same line
                if item['price'] == prevCost:
                    storeDesc_special += ', ' + item['name']
                #different price, new line, update prevCost
                else:
                    storeDesc_special += '\n`' + str(item['price']) + ' coins:` ' + item['name']
                    prevCost = item['price']

            embed.add_field(name='Special Companions', value=storeDesc_special, inline=False)

            embed.set_footer(text = 'Earn coins by participating in server events! Read #about-profiles for more information. Access this store using "+store c".')
            await ctx.send(embed = embed)
            return
        #helped
        elif type.lower() == 'helped' or type.lower() == 'h':
            storeHelp = """You can unlock these Companions with Help Points and using `+set companionName`. After reaching the minimum amount Helped, you're able to keep these Companions!"""
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
                description = 'Correct Usage: `+store [coin/helped/item]`',
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

                    embed = discord.Embed(
                        color = discord.Color.teal()
                    )

                    #ditto event
                    dittos = ['Squirtle', 'Charmander', 'Bulbasaur']
                    companion_name = c['name']
                    title = 'Consider it done! ✅'
                    value = ''

                    if companion_name in dittos:
                        if random.random() < .1:
                            companion_name = 'Ditto'
                            title = 'Consider it — Oh? **Ditto** was caught! 🌟'

                    self.dbConnection.updateProfile({"id": id}, {"$set": {"coins": coins, "companion": companion_name}})
                    embed = discord.Embed(
                        title = title,
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

        for c in self.store['Special Companions']:
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

        for i in self.store['Items']:
            if i['name'].lower() == input.lower():
                if coins >= i['price']:
                    coins -= i['price']

                    if i['name'].lower() == 'squad swap':
                        teaRole = ctx.guild.get_role(612788003542401035)
                        coffeeRole = role = ctx.guild.get_role(612788004926521365)
                        if user['squad'] == 'Coffee':
                            self.dbConnection.updateProfile({"id": id}, {"$set": {"coins": coins, "squad": 'Tea'}})
                            await ctx.author.add_roles(teaRole)
                            await ctx.author.remove_roles(coffeeRole)
                        else:
                            self.dbConnection.updateProfile({"id": id}, {"$set": {"coins": coins, "squad": 'Coffee'}})
                            await ctx.author.add_roles(coffeeRole)
                            await ctx.author.remove_roles(teaRole)

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

    @commands.command()
    async def setCompanion(self, ctx, *, companion):
        if ctx.author.id != secret.BOT_OWNER_ID:
            return
        else:
            id = ctx.author.id
            self.dbConnection.updateProfile({"id": id}, {"$set": {"companion": companion}})
            embed = discord.Embed(
                title = 'Consider it done! ✅',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

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

        companion = user['companion']
        if companion not in [c["name"] for c in self.store['Special Companions']]:
            print('Companion: ' + companion)
            embed = discord.Embed(
                title = 'You need an evolvable Special Companion to evolve!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return
        else:
            if companion == 'Eevee':
                choices = ['Flareon',
                    'Jolteon',
                    'Glaceon',
                    'Umbreon',
                    'Leafeon',
                    'Espeon',
                    'Vaporeon',
                    'Sylveon']
            elif companion == 'Cosmog':
                choices = ['Solgaleo',
                    'Lunala']
            elif companion == 'Yamper':
                choices = ['Dancing Yamper']

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

        if user is None:
            embed = discord.Embed(
                title = 'Sorry, ' + member.name + ' doesn\'t have a profile yet! They can make one by using +profile.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

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
    async def giveSquad(self, ctx, squad, amt: int, *, reason = ''):
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

    @commands.command(aliases=['helpedby', 'thanks'])
    async def rep(self, ctx):
        members = ctx.message.mentions

        for member in members:
            if ctx.author.id == member.id:
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
                        title = 'Sorry, ' + member.name + ' doesn\'t have a profile yet! They can make one by using +profile.',
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

    @commands.command(aliases=['removehelped'])
    async def derep(self, ctx):
        if not self.meta.isAdmin(ctx.author):
            return

        members = ctx.message.mentions

        for member in members:
            if ctx.author.id == member.id:
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
                        title = 'Sorry, ' + member.name + ' doesn\'t have a profile yet! They can make one by using +profile.',
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
