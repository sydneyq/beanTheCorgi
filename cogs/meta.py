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
        if 'spirits' in [role.name.lower() for role in member.roles]:
            return True
        return False

    #not allowed embed
    def noAccessEmbed(self):
        embed = discord.Embed(
            title = 'Sorry, you don\'t have permission to do that!',
            color = discord.Color.teal()
        )
        return embed

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
