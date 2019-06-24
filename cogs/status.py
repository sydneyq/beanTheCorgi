import discord
from discord.ext import commands

class Status(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def status(self, ctx, *, msg):
        if 'mods' in [role.name for role in ctx.message.author.roles] or 'mechanic' in [role.name for role in ctx.message.author.roles]:
            await self.client.change_presence(status=discord.Status.online, activity=discord.Game(msg))
        else:
            await ctx.send('You don\'t have the permissions to do that!')

def setup(client):
    client.add_cog(Status(client))
