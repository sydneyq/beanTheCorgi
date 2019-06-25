import discord
from discord.ext import commands

class AnnounceVerify(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def announceverify(self, ctx, *, msg):
        if 'mechanic' in [role.name for role in ctx.message.author.roles]:
            await ctx.send('(announceverify)')
        else:
            await ctx.send('You don\'t have the permissions to do that!')

def setup(client):
    client.add_cog(AnnounceVerify(client))
