import discord
from discord.ext import commands
from discord.utils import get
#import bot
import secret

class Meta:

    def __init__(self):
        self.OWNER = secret.BOT_OWNER_ID

    #isAdmin
    def isAdmin(self, member: discord.Member):
        if member.id == secret.BOT_OWNER_ID:
            return True
        if secret.ADMIN_ID in [role.id for role in member.roles]:
            return True
        return False

    #isStaff
    def isStaff(self, member: discord.Member):
        if member.id == secret.BOT_OWNER_ID:
                return True
        if secret.STAFF_ID in [role.id for role in member.roles]:
            return True
        return False

    #isMod
    def isMod(self, member: discord.Member):
        if member.id == secret.BOT_OWNER_ID:
            return True
        if secret.MOD_ID in [role.id for role in member.roles]:
            return True
        return False

    def isVerified(self, member: discord.Member):
        if secret.VERIFIED_ID in [role.id for role in member.roles]:
            return True
        return False

    #not allowed embed
    def noAccessEmbed(self):
        embed = discord.Embed(
            title = 'Sorry, you don\'t have permission to do that!',
            color = discord.Color.teal()
        )
        return embed

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

class Global(commands.Cog):

    def __init__(self, client, meta):
        self.client = client
        self.meta = meta

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
    async def verify(self, ctx):
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
            casual = guild.get_channel(secret.WORKSHOP_CHANNEL)
            #casual = guild.get_channel(secret.GENERAL_CHANNEL)
            msg = '**__🎉 Let\'s all welcome <@' + str(member.id) + '> to Mind Cafe! 🎉__**'
            msg += '\n> **Need Support?** Take a look at <#601444570600964097> and get started in <#597026335835291659>.'
            msg += '\n> **Want to join a Squad?** Go to <#431191485933813765> and say `+profile` to get started.'
            await casual.send(msg)
            #delete command
            await ctx.message.delete()

    @commands.command()
    async def bean(self, ctx, channel: discord.TextChannel, *, message):
        if ctx.message.author.id == secret.BOT_OWNER_ID:

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

def setup(client):
    meta_class = Meta()
    client.add_cog(Global(client, meta_class))
