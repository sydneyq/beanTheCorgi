import discord
from discord.ext import commands
from discord.utils import get
import secret
from database import Database

class Meta:

    def __init__(self, database):
        self.dbConnection = database

    def isBotOwner(self, member: discord.Member):
        if member.id == secret.BOT_OWNER_ID:
            return True
        return False

    #isAdmin
    def isAdmin(self, member: discord.Member):
        if self.isBotOwner(member):
            return True
        if secret.ADMIN_ID in [role.id for role in member.roles]:
            return True
        return False

    #isStaff
    def isStaff(self, member: discord.Member):
        if self.isBotOwner(member):
            return True
        if secret.STAFF_ID in [role.id for role in member.roles]:
            return True
        return False

    #isMod
    def isMod(self, member: discord.Member):
        if self.isBotOwner(member):
            return True
        if secret.MOD_ID in [role.id for role in member.roles]:
            return True
        return False

    #verified
    def isVerified(self, member: discord.Member):
        if secret.VERIFIED_ID in [role.id for role in member.roles]:
            return True
        return False

    #certified
    def isCertified(self, member: discord.Member):
        if secret.CERTIFIED_ID in [role.id for role in member.roles]:
            return True
        return False

    #blindfolded
    def isRestricted(self, member: discord.Member):
        if secret.RESTRICTED_ID in [role.id for role in member.roles]:
            return True
        return False

    #not allowed embed
    def embedNoAccess(self):
        embed = discord.Embed(
            title = 'Sorry, you don\'t have permission to do that!',
            color = discord.Color.teal()
        )
        return embed

    def embedDone(self):
        embed = discord.Embed(
            title = 'Consider it done! ✅',
            color = discord.Color.teal()
        )
        return embed

    def embedOops(self):
        embed = discord.Embed(
            title = 'Oops! Something went wrong.',
            color = discord.Color.teal()
        )
        return embed

    def msgWelcomeSquad(self, member: discord.Member = None):
        if member is None:
            return

        user = self.getProfile(member)
        squad = user['squad']

        msg = '**__🎉 Let\'s all welcome <@' + str(member.id) + '> to the '+squad+' Squad! 🎉__**'
        msg += '\n> Say hello to your new teammate! You\'ll be working with them during events.'
        return msg

    def getProfile(self, member: discord.Member = None):
        if member is None:
            return

        id = member.id

        profile = self.dbConnection.findProfile({"id": id})
        if profile is None:
            self.dbConnection.insertProfile({'id': id, 'squad': '', 'helped': 0, 'coins': 50, 'companion': '', 'spouse': 0, 'gifts': 0, 'affinity':''})
            profile = self.dbConnection.findProfile({"id": id})

        return profile

    def changeCoins(self, member: discord.Member, val: int):
        user = self.getProfile(member)
        coins = user['coins']
        coins += val

        #cannot afford
        if coins < 0:
            return False

        self.dbConnection.updateProfile({"id": user['id']}, {"$set": {"coins": coins}})
        return True

    def changeHelped(self, member: discord.Member, val: int):
        user = self.getProfile(member)
        helped = user['helped']
        helped += val

        #cannot afford
        if helped < 0:
            return False

        self.dbConnection.updateProfile({"id": user['id']}, {"$set": {"helped": helped}})
        return True

    def hasWord(self, string, word):
        #case-insensitive, ignores punctuation: 32-96, 123-126 (not 97 - 122)
        string = string.lower()
        word = word.lower()
        filtered = ''
        #print('string: ' + filtered)
        #print('word: ' + filtered)

        if word not in string:
            return False

        for portion in string.split():
            filtered = ''
            #print('portion: ' + filtered)
            if word in portion:
                for c in portion:
                    ascii = ord(c)
                    if ascii >= 97 and ascii <= 122:
                        filtered += c
                #print('filtered: ' + filtered)

                if filtered == word:
                    return True

        return False

    def getChannelOwnerID(self, channel: discord.TextChannel):
        return int(channel.name[channel.name.rfind('-')+1:])

    def isChannelOwner(self, member: discord.Member, channel: discord.TextChannel):
        return member.id == self.getChannelOwnerID(channel)

    def isSupportChannel(self, channel: discord.TextChannel):
        return channel.name.lower().startswith('s-')

    def isModMailChannel(self, channel: discord.TextChannel):
        return channel.name.lower().startswith('mm-')

class Global(commands.Cog):

    def __init__(self, client, database, meta):
        self.client = client
        self.meta = meta
        self.dbConnection = database

    @commands.command()
    async def ping(self, ctx):
        if (self.meta.isAdmin(ctx.message.author)):
            await ctx.send(f'Pong! `{round(self.client.latency * 1000)}ms`')

    @commands.command()
    async def status(self, ctx, *, msg):
        if (self.meta.isAdmin(ctx.message.author)):
            await self.client.change_presence(status=discord.Status.online, activity=discord.Game(msg))
        else:
            embed = discord.Embed(
                title = 'Sorry, you don\'t have permission to do that!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

    @commands.command()
    async def echo(self, ctx, channel: discord.TextChannel, *, message):
        if (self.meta.isAdmin(ctx.message.author)):

            embed = discord.Embed(
                title = 'A Mind Café Staff Member Says:',
                description = message,
                color = discord.Color.teal()
            )

            #await channel.send("**Staff Member:** " + message)
            #self.client.send_message(channel, embed=embed)
            await channel.send(embed = embed)
        else:
            embed = discord.Embed(
                title = 'Sorry, you don\'t have permission to do that!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

    @commands.command()
    async def verify(self, ctx, *, squad = None):
        member = ctx.author
        if not self.meta.isVerified(member):
            guild = ctx.guild
            #spirits
            verified_role = guild.get_role(secret.VERIFIED_ID)
            await member.add_roles(verified_role)
            #basicroles
            basicroles = guild.get_role(593065193966403587)
            await member.add_roles(basicroles)
            #helpingothers
            helpingothers = guild.get_role(593064902038650880)
            await member.add_roles(helpingothers)
            #exclusive
            exclusive = guild.get_role(593064760648663041)
            await member.add_roles(exclusive)
            #welcome
            #casual = guild.get_channel(secret.WORKSHOP_CHANNEL)
            casual = guild.get_channel(secret.GENERAL_CHANNEL)
            msg = '**__🎉 Let\'s all welcome <@' + str(member.id) + '> to Mind Cafe! 🎉__**'
            msg += '\n> **Need Support?** Take a look at <#601444570600964097> and get started in <#597026335835291659>.'
            msg += '\n> **Want to join a Squad?** Go to <#431191485933813765> and say `+profile` to get started.'
            await casual.send(msg)
            #delete command
            await ctx.message.delete()
            print(squad)
            if squad != None:
                id = member.id
                user = self.meta.getProfile(member)
                guild = ctx.guild

                if 'tea' in squad:
                    self.dbConnection.updateProfile({"id": id}, {"$set": {"squad": "Tea"}})
                    role = ctx.guild.get_role(612788003542401035)
                    await ctx.author.add_roles(role)
                    await guild.get_channel(secret.SQUAD2_CHANNEL).send(self.meta.msgWelcomeSquad(member))
                elif 'coffee' in squad:
                    self.dbConnection.updateProfile({"id": id}, {"$set": {"squad": "Coffee"}})
                    role = ctx.guild.get_role(612788004926521365)
                    await ctx.author.add_roles(role)
                    await guild.get_channel(secret.SQUAD1_CHANNEL).send(self.meta.msgWelcomeSquad(member))
                else:
                    embed = discord.Embed(
                        title = 'That Squad doesn\'t exist. Please choose either Coffee or Tea.',
                        color = discord.Color.teal()
                    )
                    await ctx.send(embed = embed, delete_after=10)
                    return

    @commands.command()
    async def bean(self, ctx, channel: discord.TextChannel, *, message):
        if self.meta.isBotOwner(ctx.author):

            embed = discord.Embed(
                description = message,
                color = discord.Color.teal()
            )

            await channel.send(embed = embed)
        else:
            embed = discord.Embed(
                title = 'Sorry, you don\'t have permission to do that!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

    #clear archive
    @commands.command(aliases=['clearA'])
    async def clearArchive(self, ctx):
        guild = self.client.get_guild(257751892241809408)
        author = ctx.message.author
        archive = 0

        if (self.meta.isAdmin(author)):
            for ch in guild.categories:
                if ch.name.lower() == 'archive':
                    archive = ch
                    break
        else:
            await ctx.send(embed = self.meta.noAccessEmbed())
            return

        for ch in archive.channels:
            await ch.delete(reason='Archive clear')

        embed = discord.Embed(
            title = 'Archive cleared! ✅',
            color = discord.Color.teal()
        )
        await ctx.send(embed = embed)

    #switch
    @commands.command(aliases=['swapST', 'swap', 'switchST'])
    async def switch(self, ctx):
        isAdmin = self.meta.isAdmin(ctx.author)
        isMod = self.meta.isMod(ctx.author)
        isCertified = self.meta.isCertified(ctx.author)
        isChannelOwner = self.meta.isChannelOwner(ctx.author, ctx.channel)
        log = ctx.guild.get_channel(secret.LOG_CHANNEL)
        channel = ctx.channel
        guild = ctx.guild

        if not isAdmin:
            if ((not isMod) and (not isChannelOwner) and (not isCertified)) or (not self.meta.isSupportChannel(channel)):
                embed = discord.Embed(
                    title = 'Sorry, that command can only be used in Support Ticket channels by the Support Ticket Owner, Certifieds, or Moderators+.',
                    color = discord.Color.teal()
                )
                await ctx.send(embed = embed)
                return

        if channel.is_nsfw():
            #change to sfw
            await channel.edit(nsfw = False)
            await channel.edit(sync_permissions = True)

            await log.send('<@' + str(ctx.author.id) + '> has switched ' + '<#' + str(channel.id) + '> to SFW.')

            embed = discord.Embed(
                title = 'Switched support channel to SFW! ✅',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
        else:
            await channel.edit(nsfw = True)
            #await newChannel.set_permissions(guild.default_role, read_messages=False)
            await channel.set_permissions(guild.get_role(secret.VERIFIED_ID), read_messages=False)
            await channel.set_permissions(self.client.get_user(self.meta.getChannelOwnerID(channel)), read_messages=True)
            await channel.set_permissions(guild.get_role(secret.NSFW_ID), read_messages=True)

            await log.send('<@' + str(ctx.author.id) + '> has switched ' + '<#' + str(channel.id) + '> to NSFW.')

            embed = discord.Embed(
                title = 'Switched support channel to NSFW! ✅',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

    #archive
    @commands.command(aliases=['archivest'])
    async def archive(self, ctx):
        isAdmin = self.meta.isAdmin(ctx.author)
        isMod = self.meta.isMod(ctx.author)
        isChannelOwner = self.meta.isChannelOwner(ctx.author, ctx.channel)
        log = ctx.guild.get_channel(secret.LOG_CHANNEL)
        channel = ctx.channel

        if not isAdmin:
            if (not isMod and not isChannelOwner) or (not self.meta.isSupportChannel(channel) and not self.meta.isModMailChannel(channel)):
                embed = discord.Embed(
                    title = 'Sorry, that command can only be used in Support Ticket channels by the Support Ticket Owner or Moderators+.',
                    color = discord.Color.teal()
                )
                await ctx.send(embed = embed)
                return

        category = 0
        for c in ctx.guild.categories:
            if c.name.lower() == 'archive':
                category = c #Archive

        if self.meta.isSupportChannel(channel) or self.meta.isModMailChannel(channel):
            user = self.client.get_user(self.meta.getChannelOwnerID(channel))

            embed = discord.Embed(
                title = 'Thanks for talking with us!',
                description = 'If you felt a Listener was supportive, you can use the command `+helpedby @user` in #botspam to show them how much you appreciated their help!',
                color = discord.Color.teal()
            )
            embed.set_thumbnail(url = 'https://cdn.discordapp.com/emojis/602887275289772052.png?v=1')

            try:
                await user.send(embed = embed)
            except:
                print('Could not send private message.')

            await log.send('Support Ticket or ModMail Ticket [**' + channel.name + '**] has been archived.')

        await ctx.message.channel.edit(name = 'archived-'+ channel.name)
        await ctx.message.channel.edit(category = category, sync_permissions = True)

    #close/delete
    @commands.command(aliases=['delete'])
    async def close(self, ctx):
        if self.meta.isAdmin(ctx.author):
            await ctx.message.channel.delete(reason='Deleted by ' + ctx.author.name)
        else:
            await ctx.send(embed = self.meta.embedNoAccess())

    #lock


    '''
    #edit msg example
    @commands.command()
    async def test(self, ctx):
        channel = ctx.guild.get_channel(612449175686086667)
        msg = channel.last_message

        if msg.author != self.client.user:
            embed = discord.Embed(
                title = 'edit me',
                color = discord.Color.teal()
            )

            await channel.send(embed = embed)
        else:
            embeds = msg.embeds
            embed = embeds[0]
            embed2 = discord.Embed(
                title = 'edited wow',
                color = discord.Color.gold()
            )

            await msg.edit(embed = embed2)
    '''

def setup(client):
    database_connection = Database()
    meta_class = Meta(database_connection)
    client.add_cog(Global(client, database_connection, meta_class))
