import discord
from discord.ext import commands
from database import Database
from .meta import Meta
import json
import os
import asyncio
import random
import secret

class Profile(commands.Cog):

    def __init__(self, client, database, meta):
        self.client = client
        self.dbConnection = database
        self.meta = meta

        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'docs/store.json')
        filename2 = os.path.join(dirname, 'docs/emojis.json')
        filename3 = os.path.join(dirname, 'docs/ids.json')

        with open(filename) as json_file:
            self.store = json.load(json_file)

        with open(filename2) as json_file:
            self.emojis = json.load(json_file)

        with open(filename3) as json_file:
            self.ids = json.load(json_file)

    def getStats(self, squad):
        tea = self.dbConnection.findProfiles({'squad' : squad})
        teaMembers = tea.count()

        #total helped
        teaHelped = 0

        #top squad member
        teaTop = ''
        teaTopHelped = 0
        teaGifted = 0
        teaTopGifted = 0
        teaTopGifter = ''
        '''
        tea_water = 0
        tea_fire = 0
        tea_air = 0
        tea_earth = 0
        '''

        for doc in tea:
            #affinities
            '''
            aff = doc['affinity'].lower()
            if aff == 'water':
                tea_water += 1
            elif aff == 'air':
                tea_air += 1
            elif aff == 'fire':
                tea_fire += 1
            elif aff == 'earth':
                tea_earth += 1
            '''
            #helped
            teaHelped += doc['helped']
            if doc['helped'] > teaTopHelped:
                teaTop = '<@' + str(doc['id']) + '> (`' + str(doc['helped']) + '` Helped)'
                teaTopHelped = doc['helped']
            elif doc['helped'] == teaTopHelped:
                teaTop += '\n<@' + str(doc['id']) + '> (`' + str(doc['helped']) + '` Helped)'

        #tea_affinities = '`' + str(tea_earth) + '` Earth | `' + str(tea_air) + '` Air | `' + str(tea_fire) + '` Fire | `' + str(tea_water) + '` Water'
        teaStr = '`' + str(teaMembers) + '` Members | `' + str(teaHelped) + '` Helped\n**Most Helpful Member(s):**\n' + teaTop
        #teaStr = '`' + str(teaMembers) + '` Members | `' + str(teaHelped) + '` Helped | `' + str(teaGifted) + '` Gifts Given\n**Most Helpful Member(s):**\n' + teaTop + '\n**Most Generous Member(s):**\n' + teaTopGifter
        return teaStr

    def getBadges(self, member: discord.Member):
        str = ''

        if self.meta.isStaff(member):
            if self.meta.isBotOwner(member):
                str = str + self.emojis['BotDeveloper'] + ' '

            if self.meta.isAdmin(member):
                str = str + self.emojis['Administrator'] + ' '
            else:
                if self.meta.isMod(member):
                    str = str + self.emojis['Moderator'] + ' '
                if self.meta.isEventCoordinator(member):
                    str = str + self.emojis['EventCoordinator'] + ' '
                if self.meta.isMarketingOfficer(member):
                    str = str + self.emojis['MarketingOfficer'] + ' '

        if self.meta.hasRole(member, 'Certifying Team'):
            str = str + self.emojis['CertifyingTeam'] + ' '

        if self.meta.isCertified(member):
            str = str + self.emojis['Certified'] + ' '

        if self.meta.hasRole(member, 'Listeners'):
            str = str + self.emojis['Listener'] + ' '

        if self.meta.hasRole(member, 'Corgi Call Responders'):
            str = str + self.emojis['CorgiCallResponder'] + ' '

        user = self.meta.getProfile(member)

        if user['helped'] >= 10:
            str = str + self.emojis['HelpPts10'] + ' '
            if user['helped'] >= 20:
                str = str + self.emojis['HelpPts20'] + ' '
                if user['helped'] >= 30:
                    str = str + self.emojis['HelpPts30'] + ' '

        if self.meta.hasRole(member, '○° bubble tea °○'):
            str = str + self.emojis['Recruited10'] + ' '

        badges = user['badges']
        for badge in badges:
            str = str + self.dbConnection.findBadge({"id":badge})['literal'] + ' '

        return str

    @commands.command(aliases=['squads', 's', 'stats', 'leaderboard'])
    async def squadCount(self, ctx):
        embed = discord.Embed(
            title = 'Squad Leaderboard',
            color = discord.Color.teal()
        )

        #emojis
        teaName = self.emojis['Tea'] + ' Tea Squad '
        coffeeName = self.emojis['Coffee'] + ' Coffee Squad '
        '''
        if teaMembers > coffeeMembers:
            teaName = teaName + ' ' + secret.PEOPLE_EMOJI
        elif teaMembers < coffeeMembers:
            coffeeName = coffeeName + ' ' + secret.PEOPLE_EMOJI

        if teaHelped > coffeeHelped:
            teaName = teaName + ' ' + secret.HELPED2_EMOJI
        elif teaHelped < coffeeHelped:
            coffeeName = coffeeName + ' ' + secret.HELPED2_EMOJI
        '''
        '''
        if tea_earth > coffee_earth:
            teaName = teaName + '🌱'
        elif tea_earth < coffee_earth:
            coffeeName = coffeeName + '🌱'

        if tea_air > coffee_air:
            teaName = teaName + '🎐'
        elif tea_air < coffee_air:
            coffeeName = coffeeName + '🎐'

        if tea_fire > coffee_fire:
            teaName = teaName + '🔥'
        elif tea_fire < coffee_fire:
            coffeeName = coffeeName + '🔥'

        if tea_water > coffee_water:
            teaName = teaName + '💧'
        elif tea_water < coffee_water:
            coffeeName = coffeeName + '💧'
        '''
        embed.add_field(name=teaName,value=self.getStats('Tea'))
        embed.add_field(name=coffeeName,value=self.getStats('Coffee'), inline=False)

        await ctx.send(embed = embed)
        return

    @commands.command(aliases=['element'])
    async def affinity(self, ctx, *, affinity = None):
        if affinity is None or (affinity.lower() != 'water' and affinity.lower() != 'fire' and affinity.lower() != 'air' and affinity.lower() != 'earth'):
            embed = discord.Embed(
                title = 'Correct Usage: `+affinity water/air/fire/earth`.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

        affinity = affinity.lower().capitalize()

        id = ctx.author.id
        user = self.meta.getProfile(ctx.author)

        if user['affinity'] is None or user['affinity'] == '':
            self.meta.changeAffinity(ctx.author, affinity)
            await ctx.send(embed = self.meta.embedDone())
            return
        else:
            embed = discord.Embed(
                title = 'You already have an affinity!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

    @commands.command()
    async def givebadge(self, ctx, member: discord.Member, *, badge):
        if not self.meta.isAdmin(ctx.author):
            return
        else:
            self.meta.addBadgeToProfile(member, badge)
            await ctx.send(embed = self.meta.embedDone())

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

        id = ctx.author.id
        user = self.meta.getProfile(ctx.author)
        guild = ctx.guild

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
                await guild.get_channel(self.ids['SQUAD_TEA_CHANNEL']).send(self.meta.msgWelcomeSquad(ctx.author))
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
                await guild.get_channel(self.ids['SQUAD_COFFEE_CHANNEL']).send(self.meta.msgWelcomeSquad(ctx.author))
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
        user = self.meta.getProfile(ctx.author)

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
            member = ctx.author
        else:
            id = other.id
            member = other

        user = self.meta.getProfile(member)
        pic = member.avatar_url
        name = member.name

        #Basics
        if (user['squad'] == "Tea"):
            embed = discord.Embed(color=0xe99c3e)
            embed.add_field(name="Squad", value=self.emojis['Tea'] + ' ' + user['squad'], inline=True)
            embed.set_author(name = name, icon_url = 'https://cdn2.stylecraze.com/wp-content/uploads/2015/04/2072_11-Surprising-Benefits-And-Uses-Of-Marijuana-Tea_shutterstock_231770824.jpg')
        elif (user['squad'] == "Coffee"):
            embed = discord.Embed(color=0xace605)
            embed.add_field(name="Squad", value=self.emojis['Coffee'] + ' ' + user['squad'], inline=True)
            embed.set_author(name = name, icon_url = 'https://www.caffesociety.co.uk/assets/recipe-images/latte-small.jpg')
        else:
            embed = discord.Embed(color = discord.Color.teal())
            embed.add_field(name="Squad", value='No Squad yet. Use `+squad tea/coffee` to join one!', inline=True)
            embed.set_author(name = name)

        if user['affinity'] == '':
            msg2 = 'No affinity yet. Set one with `+affinity`!'
        else:
            msg2 = user['affinity']
            emoji = ''
            if msg2 == 'Fire':
                emoji = self.emojis['Fire']
            elif msg2 == 'Earth':
                emoji = self.emojis['Earth']
            elif msg2 == 'Air':
                emoji = self.emojis['Air']
            elif msg2 == 'Water':
                emoji = self.emojis['Water']
            msg2 = emoji + ' ' + msg2
        embed.add_field(name='Affinity', value=msg2, inline=True)

        embed.set_footer(text = 'Mind Café', icon_url = 'https://media.discordapp.net/attachments/591611902459641856/593267453363224588/Bean_Icon.png')

        #Marriage
        if user['spouse'] == 0:
            spouse = 'N/A'
        else:
            spouse = '<@' + str(user['spouse']) + '>'
        embed.add_field(name="Soulmate", value=spouse, inline=True)

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
                for c in self.store['Evolvable Companions']:
                    if c['name'].lower() == companion.lower():
                        embed.set_image(url = c['src'])
                        isFound = True
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
                msg = self.emojis['Special'] + ' ' + companion
        else:
            msg = 'No companion yet. Get one at `+store`!'

        embed.add_field(name="Companion", value=msg, inline=True)

        #Acknowledgements
        badges = self.getBadges(member)
        numBadges = 0
        if badges == '':
            badges = 'No badges yet.'
        else:
            numBadges = badges.count('<')
        embed.add_field(name="Badges (`" + str(numBadges) + "`)", value=badges, inline=True)

        embed.set_thumbnail(url = pic)
        await ctx.send(embed=embed)

    @commands.command(alises=['spouses', 'spouse', 'soulmate', 'marriages'])
    async def soulmates(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        user = self.meta.getProfile(member)
        soulmates = user['soulmates']

        num = self.meta.getNumSoulmates(member)
        soulmate_spots = self.meta.getSoulmateSpots(member)
        desc = ''
        for soulmate in soulmates:
            desc += '<@' + str(soulmate) + '>\n'

        if desc == '':
            desc = 'N/A'

        embed = discord.Embed(
            title = member.name + '\'s Marriages `[' + str(num) + '/' + str(soulmate_spots)  + ']`',
            description = desc,
            color = discord.Color.teal()
        )
        embed.set_footer(text = 'For every 10 Help Points, you gain a soulmate spot!')
        await ctx.send(embed = embed)
        return

    @commands.command(alias=['propose'])
    async def marry(self, ctx, member: discord.Member = None):
        if member is None:
            embed = discord.Embed(
                description = 'Correct Usage: `+marry @user`.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

        if ctx.author.bot or member.bot:
            embed = discord.Embed(
                title = 'You can\'t marry a bot!',
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

        id = ctx.author.id

        user = self.meta.getProfile(ctx.author)
        memberProfile = self.meta.getProfile(member)

        if not self.meta.canAddSoulmate(ctx.author) or not self.meta.canAddSoulmate(member):
            embed = discord.Embed(
                title = 'One of you doesn\'t have enough soulmate spots!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return
        '''
        user_spots = int(user['helped']) / 10
        memberProfile

        if user['spouse'] != 0 or memberProfile['spouse'] != 0:
            embed = discord.Embed(
                title = 'One of you is already married!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return
        '''

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

            confirmed = self.meta.addSoulmate(ctx.author, member)
            if not (confirmed):
                await ctx.send(embed = self.meta.embedOops())
                return

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
    async def divorce(self, ctx, member: discord.Member = None):
        id = ctx.author.id
        user = self.meta.getProfile(ctx.author)

        soulmates = user['soulmates']

        if len(soulmates) == 0:
            await ctx.send(embed = self.meta.embedOops())
            return

        if member is None:
            member = soulmates[0]
        else:
            if member.id not in soulmates:
                await ctx.send(embed = self.meta.embedOops())
                return
            else:
                member = member.id

        spouse_name = 'spouse'
        spouseExists = False
        if self.meta.profileDoesExist(spouse):
            spouseExists = True
            spouse_name = self.client.get_user(member).name

        embed = discord.Embed(
            title = 'Divorce ' + spouse_name + '?',
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

            self.meta.removeSoulmate(ctx.author, member)
            '''
            soulmates.remove(member)
            self.dbConnection.updateProfile({"id": ctx.author.id}, {"$set": {"soulmates": soulmates}})

            if spouseExists:
                memberProfile = self.meta.getProfile(member)
                member_soulmates = memberProfile['soulmates']
                member_soulmates.remove(ctx.author.id)
                self.dbConnection.updateProfile({"id": spouse}, {"$set": {"soulmates": member_soulmates}})
            '''

            embed = discord.Embed(
                title = 'Divorced ' + spouse_name + '.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        id = member.id
        user = self.meta.getProfile(member)
        if user['spouse'] != 0:
            self.dbConnection.updateProfile({"id": user['spouse']}, {"$set": {"spouse": 0}})
        self.dbConnection.removeProfile({"id": id})

def setup(client):
    database_connection = Database()
    meta_class = Meta(database_connection)
    client.add_cog(Profile(client, database_connection, meta_class))
